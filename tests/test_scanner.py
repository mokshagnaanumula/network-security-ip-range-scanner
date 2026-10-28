import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scanner


class RangeScannerTests(unittest.TestCase):
    def test_rejects_large_networks_and_ipv6(self):
        for cidr in ("192.168.0.0/16", "2001:db8::/64"):
            with self.subTest(cidr=cidr), self.assertRaises(ValueError):
                scanner.parse_network(cidr)
        self.assertEqual(str(scanner.parse_network("192.168.1.0/28")), "192.168.1.0/28")

    @patch("scanner.platform.system", return_value="Linux")
    @patch("scanner.subprocess.run", return_value=subprocess.CompletedProcess([], 0))
    def test_probe_reports_active_on_reply(self, run, system):
        import ipaddress
        self.assertEqual(scanner.probe(ipaddress.ip_address("192.0.2.1"), .2), ("192.0.2.1", "active"))
        run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
