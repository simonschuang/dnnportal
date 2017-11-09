# Copyright (c) 2015-2017, NVIDIA CORPORATION.  All rights reserved.
from __future__ import absolute_import

from . import option_list
import dnnport.device_query


option_list['gpu_list'] = ','.join([str(x) for x in xrange(len(dnnport.device_query.get_devices()))])
