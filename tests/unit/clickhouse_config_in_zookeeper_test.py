import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from aws_lambda_context import LambdaContext

from src.handler import get_clickhouse_cluster_definition
from src.handler import get_ec2_client
from src.handler import get_zookeeper_client
from src.handler import lambda_handler


class GetZookeeperClient(unittest.TestCase):
    @patch("src.handler.KazooClient")
    def test_gets_network_interfaces_for_telemetry_zookeeper_and_creates_kazoo_client_with_ips(
        self, mock_kazoo_constructor
    ):
        mock_kazoo_client = MagicMock()
        mock_kazoo_constructor.return_value = mock_kazoo_client
        ec2_client = MagicMock()
        ec2_client.describe_network_interfaces = MagicMock(
            return_value={
                "NetworkInterfaces": [
                    {"PrivateIpAddress": "192.168.1.1"},
                    {"PrivateIpAddress": "192.168.1.2"},
                    {"PrivateIpAddress": "192.168.1.3"},
                ]
            }
        )

        self.assertEqual(get_zookeeper_client(ec2_client), mock_kazoo_client)

        ec2_client.describe_network_interfaces.assert_called_with(
            Filters=[
                {"Name": "tag:Component", "Values": ["telemetry-zookeeper"]},
                {"Name": "status", "Values": ["in-use"]},
            ]
        )
        mock_kazoo_client.start.assert_called_once()
        mock_kazoo_constructor.assert_called_with(
            hosts=["192.168.1.1", "192.168.1.2", "192.168.1.3"]
        )


class GetClickhouseClusterDefinition(unittest.TestCase):
    def test_get_all_clickhouse_shards_to_instances(self):
        ec2_client = MagicMock()
        ec2_client.describe_instances = MagicMock(
            return_value={
                "Reservations": [
                    {
                        "Instances": [
                            {
                                "PrivateIpAddress": "172.26.39.30",
                                "Tags": [
                                    {"Value": "integration", "Key": "Env"},
                                    {"Value": "1", "Key": "clickhouse-server"},
                                    {
                                        "Value": "clickhouse-server-shard_1_replica_1-asg-2018102612411970390000000d",
                                        "Key": "aws:autoscaling:groupName",
                                    },
                                    {"Value": "webops_engineer", "Key": "iam-groups"},
                                    {
                                        "Value": "clickhouse-server-shard_1_replica_1",
                                        "Key": "Name",
                                    },
                                    {
                                        "Value": "team-webops",
                                        "Key": "sensu-team-handler",
                                    },
                                    {"Value": "shard_1", "Key": "shard_name"},
                                    {"Value": "false", "Key": "tls"},
                                    {
                                        "Value": "arn:aws:iam::638924580364:role/RoleCrossAccountSSH",
                                        "Key": "auth-account-arn",
                                    },
                                ],
                            }
                        ],
                    },
                    {
                        "Instances": [
                            {
                                "PrivateIpAddress": "172.26.32.16",
                                "Tags": [
                                    {
                                        "Value": "clickhouse-server-shard_2_replica_1-asg-2018102612415581190000000f",
                                        "Key": "aws:autoscaling:groupName",
                                    },
                                    {"Value": "integration", "Key": "Env"},
                                    {"Value": "webops_engineer", "Key": "iam-groups"},
                                    {
                                        "Value": "team-webops",
                                        "Key": "sensu-team-handler",
                                    },
                                    {"Value": "false", "Key": "tls"},
                                    {
                                        "Value": "clickhouse-server-shard_2_replica_1",
                                        "Key": "Name",
                                    },
                                    {
                                        "Value": "arn:aws:iam::638924580364:role/RoleCrossAccountSSH",
                                        "Key": "auth-account-arn",
                                    },
                                    {"Value": "shard_2", "Key": "shard_name"},
                                    {"Value": "1", "Key": "clickhouse-server"},
                                ],
                                "AmiLaunchIndex": 0,
                            }
                        ],
                    },
                    {
                        "Instances": [
                            {
                                "PrivateIpAddress": "172.26.99.237",
                                "Tags": [
                                    {
                                        "Value": "team-webops",
                                        "Key": "sensu-team-handler",
                                    },
                                    {
                                        "Value": "arn:aws:iam::638924580364:role/RoleCrossAccountSSH",
                                        "Key": "auth-account-arn",
                                    },
                                    {"Value": "webops_engineer", "Key": "iam-groups"},
                                    {"Value": "false", "Key": "tls"},
                                    {
                                        "Value": "clickhouse-server-shard_1_replica_2-asg-2018102612412156150000000e",
                                        "Key": "aws:autoscaling:groupName",
                                    },
                                    {"Value": "integration", "Key": "Env"},
                                    {
                                        "Value": "clickhouse-server-shard_1_replica_2",
                                        "Key": "Name",
                                    },
                                    {"Value": "1", "Key": "clickhouse-server"},
                                    {"Value": "shard_1", "Key": "shard_name"},
                                ],
                                "AmiLaunchIndex": 0,
                            }
                        ]
                    },
                    {
                        "Instances": [
                            {
                                "PrivateIpAddress": "172.26.97.29",
                                "Tags": [
                                    {
                                        "Value": "clickhouse-server-shard_2_replica_2-asg-20181026124228126900000010",
                                        "Key": "aws:autoscaling:groupName",
                                    },
                                    {
                                        "Value": "clickhouse-server-shard_2_replica_2",
                                        "Key": "Name",
                                    },
                                    {"Value": "1", "Key": "clickhouse-server"},
                                    {
                                        "Value": "arn:aws:iam::638924580364:role/RoleCrossAccountSSH",
                                        "Key": "auth-account-arn",
                                    },
                                    {"Value": "webops_engineer", "Key": "iam-groups"},
                                    {
                                        "Value": "team-webops",
                                        "Key": "sensu-team-handler",
                                    },
                                    {"Value": "shard_2", "Key": "shard_name"},
                                    {"Value": "false", "Key": "tls"},
                                    {"Value": "integration", "Key": "Env"},
                                ],
                            }
                        ]
                    },
                ]
            }
        )

        self.assertEqual(
            get_clickhouse_cluster_definition(ec2_client),
            {
                "shard_1": ["172.26.39.30", "172.26.99.237"],
                "shard_2": ["172.26.32.16", "172.26.97.29"],
            },
        )

        ec2_client.describe_instances.assert_called_with(
            Filters=[
                {"Name": "tag-key", "Values": ["clickhouse-server"]},
                {"Name": "instance-state-name", "Values": ["running"]},
            ]
        )


class LambdaHandler(unittest.TestCase):
    @patch("src.handler.get_clickhouse_cluster_definition")
    @patch("src.handler.get_zookeeper_client")
    @patch("src.handler.get_ec2_client")
    def test_should_ensure_zookeeper_path_exists_for_remote_servers(
        self,
        mock_get_ec2_client,
        mock_get_zookeeper_client,
        mock_get_clickhouse_cluster_definition,
    ):
        zookeeper = MagicMock()
        mock_get_zookeeper_client.return_value = zookeeper
        lambda_context = LambdaContext()
        lambda_context.function_name = "lambda_handler"
        lambda_context.aws_request_id = "abc-123"

        lambda_handler({}, lambda_context)

        zookeeper.ensure_path.assert_any_call("clickhouse.config.remote_servers")

    @patch(
        "src.handler.get_clickhouse_cluster_definition",
        return_value="pumpkins",
    )
    @patch("src.handler.get_zookeeper_client")
    @patch("src.handler.get_ec2_client")
    def test_all_private_ips_and_shards_matching_clickhouse_server_added_to_zookeeper(
        self,
        mock_get_ec2_client,
        mock_get_zookeeper_client,
        mock_get_clickhouse_cluster_definition,
    ):
        ec2_client = MagicMock()
        mock_get_ec2_client.return_value = ec2_client
        shard_config = {
            "shard_1": ["172.26.39.30", "172.26.99.237"],
            "shard_2": ["172.26.32.16", "172.26.97.29"],
        }
        mock_get_clickhouse_cluster_definition.return_value = shard_config
        zookeeper = MagicMock()
        mock_get_zookeeper_client.return_value = zookeeper
        lambda_context = LambdaContext()
        lambda_context.function_name = "lambda_handler"
        lambda_context.aws_request_id = "abc-123"

        result = lambda_handler({}, lambda_context)

        remote_servers_xml = b"""<hmrc_data_cluster>
  <shard>
    <internal_replication>true</internal_replication>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.39.30</host>
      <port>9000</port>
    </replica>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.99.237</host>
      <port>9000</port>
    </replica>
  </shard>
  <shard>
    <internal_replication>true</internal_replication>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.32.16</host>
      <port>9000</port>
    </replica>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.97.29</host>
      <port>9000</port>
    </replica>
  </shard>
</hmrc_data_cluster>"""

        zookeeper.set.assert_any_call(
            "clickhouse.config.remote_servers", remote_servers_xml
        )
        self.assertEqual(result, {"cluster_definition": shard_config})


class GetEC2Client(unittest.TestCase):
    @patch("src.handler.boto3")
    def test_check_get_ec2_client_returns_correct_type_of_object(self, mock_boto3):
        expected_response = MagicMock()
        mock_boto3.client.return_value = expected_response

        ec2 = get_ec2_client()

        mock_boto3.client.assert_called_with("ec2", "eu-west-2")
        self.assertEqual(expected_response, ec2)
