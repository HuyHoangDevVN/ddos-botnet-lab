"""
Safe lab preflight and deployment checks.
"""
import logging

from core.config import LabConfig
from core.safety import consent_banner, validate_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LabDeployer:
    def __init__(self, config: LabConfig):
        self.config = config

    def deploy_all(self) -> None:
        logger.info("[*] Starting safe-lab preflight...")
        logger.warning("\n%s\n", consent_banner())
        validate_config(self.config)
        logger.info("[+] Safe-lab preflight checks passed")


if __name__ == '__main__':
    deployer = LabDeployer(LabConfig.from_env())
    deployer.deploy_all()
