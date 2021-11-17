"""
The ``sensortoolkit.deploy`` subpackage contains modules for creating and
populating the deployment dictionary data structure and other deployment-related
methods for characterizing the deployment conditions and duration.

===============================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Last Updated:
  Thu Aug 19 10:58:00 2021
"""

from ._create_deploy_dict import (construct_deploy_dict,
                                  deploy_met_stats, deploy_ref_stats)
from ._deployment_period import deployment_period
from ._get_max_conc import get_max_conc
