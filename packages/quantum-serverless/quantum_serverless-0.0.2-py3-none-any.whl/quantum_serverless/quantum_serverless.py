# This code is a Qiskit project.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
=================================================================
Quantum serverless (:mod:`quantum_serverless.quantum_serverless`)
=================================================================

.. currentmodule:: quantum_serverless.quantum_serverless

Quantum serverless
==================

.. autosummary::
    :toctree: ../stubs/

    BaseQuantumServerless
    QuantumServerless
"""
import json
import logging
import os
from abc import ABC
from typing import Optional, Union, List, Dict, Any

import requests
from qiskit import IBMQ
from qiskit.providers import Backend
from ray._private.worker import BaseContext

from quantum_serverless.core.provider import Provider, Cluster
from quantum_serverless.exception import QuantumServerlessException
from quantum_serverless.serializers import register_all_serializers

Context = Union[BaseContext]


class BaseQuantumServerless(ABC):
    """BaseQuantumServerless class."""

    @classmethod
    def load_configuration(cls, path: str) -> "BaseQuantumServerless":
        """Creates QuantumServerless object from configuration."""
        raise NotImplementedError

    def provider(
        self,
        provider: Union[str, Provider],
        cluster: Optional[Union[str, Cluster]] = None,
    ) -> Context:
        """Allocate context with selected provider and cluster.

        Example:
            >>> quantum_serverless = QuantumServerless()
            >>> with quantum_serverless.provider("ibm"):
            >>>     ...

        Args:
            provider: provider or name of provider to use for context allocation
            cluster: cluster or name of cluster within provider to use for context allocation

        Returns:
            Execution context
        """
        raise NotImplementedError

    def cluster(self, cluster: Union[str, Cluster]) -> Context:
        """Allocate context with selected cluster.

        Example:
            >>> quantum_serverless = QuantumServerless()
            >>> with quantum_serverless.cluster("<MY_CLUSTER>"):
            >>>     ...

        Args:
            cluster: cluster or name of cluster within provider to use for context allocation

        Returns:
            Execution context.
        """
        raise NotImplementedError

    def add_provider(self, provider: Provider) -> "BaseQuantumServerless":
        """Adds provider."""
        raise NotImplementedError

    def set_provider(
        self, provider: Union[str, int, Provider]
    ) -> "BaseQuantumServerless":
        """Set specific provider."""
        raise NotImplementedError

    def providers(self) -> List[Provider]:
        """Returns list of available providers."""
        raise NotImplementedError

    def clusters(self) -> List[Cluster]:
        """Returns list of available clusters."""
        raise NotImplementedError

    def backends(self, **kwargs) -> List[Backend]:
        """Returns list of available backends."""
        raise NotImplementedError

    def add_cluster(self, cluster: Cluster) -> "BaseQuantumServerless":
        """Adds cluster to list of available clusters

        Args:
            cluster: cluster to add

        Returns:
            self reference
        """
        raise NotImplementedError

    def set_cluster(self, cluster: Union[int, str, Cluster]) -> "BaseQuantumServerless":
        """Sets cluster to use for context.

        Args:
            cluster: Can be int for index in list,
                str for name of cluster in list
                or Cluster object.

        Returns:
            self reference
        """
        raise NotImplementedError

    def context(self, **kwargs) -> Context:
        """Creates execution context for serverless workloads."""
        raise NotImplementedError


class QuantumServerless(BaseQuantumServerless):
    """QuantumServerless class."""

    @classmethod
    def load_configuration(cls, path: str) -> "QuantumServerless":
        """Creates instance from configuration file.

        Example:
            >>> quantum_serverless = QuantumServerless.load_configuration("./my_config.json")

        Args:
            path: path to file with configuration

        Returns:
            Instance of QuantumServerless
        """
        with open(path, "r") as config_file:  # pylint: disable=unspecified-encoding
            config = json.load(config_file)
            return QuantumServerless(config)

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Quantum serverless management class.

        Example:
            >>> configuration = {"providers": [
            >>>    {"name": "<NAME>", "host": "<HOST>", "token": "<TOKEN>"}
            >>> ]}
            >>> quantum_serverless = QuantumServerless(configuration)

        Example:
            >>> quantum_serverless = QuantumServerless()

        Args:
            config: configuration

        Example:
            >>> from quantum_serverless import QuantumServerless
            >>> serverless = QuantumServerless()

        Raises:
            QuantumServerlessException
        """
        self._providers: List[Provider] = load_config(config)
        self._selected_provider: Provider = self._providers[-1]
        self._clusters = [
            provider.cluster for provider in self._providers if provider.cluster
        ]
        self._selected_cluster: Cluster = self._selected_provider.cluster

        self._allocated_context: Optional[Context] = None

    def __enter__(self):
        self._allocated_context = self._selected_cluster.context()
        return self._allocated_context

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._allocated_context:
            self._allocated_context.disconnect()

    def provider(
        self,
        provider: Union[str, Provider],
        cluster: Optional[Union[str, Cluster]] = None,
        **kwargs,
    ) -> Context:
        if isinstance(cluster, Cluster):
            return cluster.context(**kwargs)

        if isinstance(provider, Provider) and provider.cluster is None:
            raise QuantumServerlessException("Given provider does not have cluster")

        if isinstance(provider, str):
            available_providers: Dict[str, Provider] = {
                p.name: p for p in self._providers
            }
            if provider in available_providers:
                provider = available_providers[provider]
            else:
                raise QuantumServerlessException(
                    f"Provider {provider} is not in a list of available providers "
                    f"{list(available_providers.keys())}"
                )

        if cluster is None:
            return provider.context(**kwargs)

        available_clusters: Dict[str, Cluster] = {
            c.name: c for c in provider.available_clusters
        }
        if cluster in available_clusters:
            return available_clusters[cluster].context(**kwargs)

        raise QuantumServerlessException(
            f"Cluster {cluster} is not in a list of available clusters "
            f"{list(available_clusters.keys())}"
        )

    def cluster(self, cluster: Union[str, Cluster], **kwargs) -> Context:
        if isinstance(cluster, Cluster):
            return cluster.context(**kwargs)
        if isinstance(cluster, str):
            available_clusters: Dict[str, Cluster] = {c.name: c for c in self._clusters}
            if cluster in available_clusters:
                return available_clusters[cluster].context(**kwargs)

            raise QuantumServerlessException(
                f"No cluster named {cluster} in list of available clusters"
                f"{list(available_clusters.keys())}"
            )

        raise QuantumServerlessException(
            "Argument must be instance of Cluster or str with name of available cluster."
        )

    def add_provider(self, provider: Provider) -> "BaseQuantumServerless":
        self._providers.append(provider)
        return self

    def set_provider(
        self, provider: Union[str, int, Provider]
    ) -> "BaseQuantumServerless":
        providers = self._providers
        if isinstance(provider, int):
            if len(providers) <= provider:
                raise QuantumServerlessException(
                    f"Selected index is out of bounds. "
                    f"You picked {provider} index whereas only {len(providers)}"
                    f"available"
                )
            self._selected_provider = providers[provider]

        elif isinstance(provider, str):
            provider_names = [c.name for c in providers]
            if provider not in provider_names:
                raise QuantumServerlessException(
                    f"{provider} name is not in a list "
                    f"of available provider names: {provider_names}."
                )
            self._selected_provider = providers[provider_names.index(provider)]

        elif isinstance(provider, Provider):
            self._selected_provider = provider

        if self._selected_provider.cluster:
            self._selected_cluster = self._selected_provider.cluster

        return self

    def providers(self) -> List[Provider]:
        return self._providers

    def clusters(self) -> List[Cluster]:
        return self._clusters

    def backends(self, **kwargs) -> List[Backend]:
        provider = IBMQ.load_account()
        return provider.backends()

    def add_cluster(self, cluster: Cluster) -> "BaseQuantumServerless":
        if cluster in self._clusters:
            logging.warning(
                "%s cluster already in list of available clusters. Skipping addition...",
                cluster.name,
            )
        else:
            self._clusters.append(cluster)
        return self

    def set_cluster(self, cluster: Union[int, str, Cluster]) -> "QuantumServerless":
        clusters = self._clusters
        if isinstance(cluster, int):
            if len(clusters) <= cluster:
                raise QuantumServerlessException(
                    f"Selected index is out of bounds. "
                    f"You picked {cluster} index whereas only {len(clusters)}"
                    f"available"
                )
            self._selected_cluster = clusters[cluster]

        elif isinstance(cluster, str):
            cluster_names = [c.name for c in clusters]
            if cluster not in cluster_names:
                raise QuantumServerlessException(
                    f"{cluster} name is not in a list "
                    f"of available cluster names: {cluster_names}."
                )
            self._selected_cluster = clusters[cluster_names.index(cluster)]

        elif isinstance(cluster, Cluster):
            self._selected_cluster = cluster

        return self

    def context(self, **kwargs) -> Context:
        """Returns Ray context for tasks/actors execution."""
        # register custom serializers
        register_all_serializers()

        return self._selected_cluster.context(**kwargs)

    def __repr__(self):
        providers = ", ".join(provider.name for provider in self.providers())
        clusters = ", ".join(cluster.name for cluster in self.clusters())
        return f"<QuantumServerless: providers [{providers}], clusters [{clusters}]>"


def load_config(config: Optional[Dict[str, Any]] = None) -> List[Provider]:
    """Loads providers from configuration."""
    local_provider = Provider(
        name="local",
        cluster=Cluster(name="local"),
        available_clusters=[Cluster(name="local")],
    )
    providers = [local_provider]

    if config is not None:
        for provider_config in config.get("providers", []):
            cluster = None
            if provider_config.get("cluster"):
                cluster = Cluster(**provider_config.get("cluster"))

            available_clusters = []
            if provider_config.get("available_clusters"):
                for cluster_json in provider_config.get("available_clusters"):
                    available_clusters.append(Cluster(**cluster_json))
            providers.append(
                Provider(
                    **{
                        **provider_config,
                        **{
                            "cluster": cluster,
                            "available_clusters": available_clusters,
                        },
                    }
                )
            )

    if os.environ.get("QS_CLUSTER_MANAGER_ADDRESS", None):
        auto_discovered_provider = get_auto_discovered_provider(
            manager_address=os.environ.get("QS_CLUSTER_MANAGER_ADDRESS"),
            token=os.environ.get("QS_CLUSTER_MANAGER_TOKEN"),
        )
        if auto_discovered_provider is not None:
            providers.append(auto_discovered_provider)

    return providers


def get_auto_discovered_provider(
    manager_address: str, token: Optional[str] = None
) -> Optional[Provider]:
    """Makes http request to manager to get available clusters."""
    clusters = []

    headers = {"Authorization": f"Bearer {token}"} if token else None
    url = f"{manager_address}/quantum-serverless-manager/cluster/"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.ok:
            cluster_names_response = json.loads(response.text)
            for cluster_name in cluster_names_response:
                name = cluster_name.get("name")
                cluster_details_response = requests.get(
                    f"{url}{name}", headers=headers, timeout=10
                )
                if cluster_details_response.ok and name:
                    clusters.append(
                        Cluster.from_dict(json.loads(cluster_details_response.text))
                    )
        else:
            logging.warning(
                "Something went wrong when trying to connect to provider: [%d] %s",
                response.status_code,
                response.text,
            )

    except Exception:  # pylint: disable=broad-except
        logging.info(
            "Autodiscovery: was not able to autodiscover additional resources."
        )

    if len(clusters) > 0:
        return Provider(
            name="auto_discovered", cluster=clusters[0], available_clusters=clusters
        )

    return None
