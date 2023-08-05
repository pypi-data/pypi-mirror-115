#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2020 Huawei Technologies Co., Ltd
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import acl
import os
from ..common.const import *
from ..common.log import Log


def acl_vesion(self):
    """ get acl version of system intalled. 

    Args:
        None

    Returns:
        major_ver : major version 
        minor_ver : created stream or original
        patch_ver :
    """
    major_ver, minor_ver, patch_ver, ret = acl.get_version()
    if ret != ACL_SUCCESS:
        raise ValueError(f"pyACL is not installed or invalid.")

    version = str(major_ver) + '.' + str(minor_ver) + '.' + str(patch_ver)
    return version

def run_mode():
    """ get run mode of Ascend310. 

    Args:
        None

    Returns:
        run_mode : 0 for evaluate board or Atlas200 on ctrl-cpu, 1 for standard Inference 
            card(Atlas300-3000/Atlas300-3010/Atlas800-3000/Atlas500/Atlas500pro) on host-cpu

    """
    run_mode, ret = acl.rt.get_run_mode()
    if ret != ACL_SUCCESS:
        raise ValueError(f"pyACL is not installed or isinvalid.")

    return run_mode


def device_num():
    """ get device number of the system

    Args:
        None

    Returns:
        device_num : 0 for evaluate board or Atlas200 on ctrl-cpu, 1 for standard Inference 
            card(Atlas300-3000/Atlas300-3010/Atlas800-3000/Atlas500/Atlas500pro) on host-cpu
    """
    count, ret = acl.rt.get_device_count()
    if ret != ACL_SUCCESS:
        raise ValueError(f"pyACL is not installed or Atlas device is not working well.")

    return count


def create_stream(context=None):
    """ create a stream. 
        case 1. context is None. Get the context and create a new stream.
        case 2. context is not None. Create a new stream on existing context.
    Args:
        context.

    Returns:
        context : 
        stream  : created stream or original
    """
    if context is None:
        context, ret = acl.rt.get_context()
        assert ret == ACL_SUCCESS, f"get context failed in bind_stream, return {ret}."

    ret = acl.rt.set_context(context)
    if ret != ACL_SUCCESS:
        raise ValueError(f"acl set context failed, return {ret}.")

    stream, ret = acl.rt.create_stream()
    if ret != ACL_SUCCESS:
        raise ValueError(f"create stream failed in create_stream, return {ret}.")
    
    Log(INFO, f"Create stream at context {context} success.")
    return stream


def bind_context(context):
    """ Binding an existing context. If context is not exist, raise an error else set this context.
    Args:
        context.

    Returns:
        None.
    """
    if context is None:
        context, ret = acl.rt.get_context()
        assert ret == ACL_SUCCESS, f"get context failed in bind_context, return {ret}."
    
    ret = acl.rt.set_context(context)
    if ret != ACL_SUCCESS:
        raise ValueError(f"acl set context failed in bind_context,, return {ret}.")

    Log(INFO, f"Set context {context} success.")
    return ret


class Context():
    """Define a Context class to manage context of device.

    attr:
        devices (set)      : save the device configured.
        context_dict (dict): a dict save the map of device id and context.

    function:
        __check_para    : check input parameters whether in law or not
        __init_resource : initial the device.
        __create_context: create context according to configured device, and 
                          save it to context_dict.

    EXAMPLE:
        devices = {0,1,2,3}

        context_dict = {0:[contex0], 
                        1:[contex1], 
                        2:[contex2], 
                        3:[contex3]}

        (stream_dict not release)
        stream_dict = {contex0:[stream00, stream01],
                    contex1:[stream10, stream11],
                    contex2:[stream20, stream21],
                    contex3:[stream30, stream31]}
    """
    def __init__(self, device, acl_json=None):
        self.class_name = self.__class__.__name__

        if type(self)._first:
            # check input parameters
            self.__check_para(device)

            self.devices = set(device)
            self.context_dict = {}
            self.device_num = 0

            # initial device context resource
            self.__init_resource(acl_json)
            self.__create_context()


    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):   
            cls._inst = super(Context, cls).__new__(cls)
            cls._first = True
        else:
            cls._first = False
            Log(WARNING, 'Context is already instantiated')
        return cls._inst

    def __iter__(self):
        self.iter = iter(self.context_dict.values())
        return self.iter

    def __next__(self):
        return next(self.iter)


    def __check_para(self, devices):
        """ check input device is in [0, device_num - 1].
        Args:
            devices : input device

        Returns:
            None.
        """
        if not isinstance(devices, (list, set, tuple)):
            raise TypeError(f"Input device expects a list/tuple/set, but got {type(devices)}.")

        if len(devices) == 0:
            raise ValueError(f"Input device is null.")

        self.device_num, ret = acl.rt.get_device_count()
        if ret != ACL_SUCCESS:
            raise ValueError(f"Fail to get device in func __check_para, maybe device is \
                        not exist, return {ret}.")
   
        if self.device_num < len(devices):
            raise ValueError(f"Input param 'device' error in func __check_para, \
                        because the elements of device-set exceed {self.device_num}.") 

        # below we not sure this method is better
        assert sorted(devices)[0] >= 0 and sorted(devices)[-1] < self.device_num, \
            f"Device id {device_id} is out of range [0, {self.device_num})."
   

    def __init_resource(self, acl_json=None):
        """initial device resource according to acl_json file.
        Args:
            acl_json : the file path of acl_json.

        Returns:
            None.
        """
        if acl_json is None:
            ret = acl.init()  
        elif os.path.exists(acl_json):
            ret = acl.init(acl_json)
        else:
            raise ValueError(f"Fail to open a not existing acl_json file:{acl_json}.")

        if ret != ACL_SUCCESS:
            raise ValueError(f"Fail to init acl in func __init_resource, return {ret}.")

    def __create_context(self):
        """ create a context according to input device, and save them to context_dict.
        Args:
            None.

        Returns:
            None.
        """
        for device_id in self.devices:
            ret = acl.rt.set_device(device_id)
            if ret != ACL_SUCCESS:
                raise ValueError(f"Set device {device_id} failed in func \
                            __create_context, return {ret}.")

            context, ret = acl.rt.create_context(device_id)
            if ret != ACL_SUCCESS:
                raise ValueError(f"Create context failed on device {device_id}, return {ret}.")

            # save the created context to dict
            self.context_dict[device_id] = context

    @classmethod
    def runmode(self, device_id):
        if not isinstance(device_id, int):
            raise TypeError('device_id expects an int value, '
                                f'but received {type(device_id)}')

        assert (device_id >= 0) and (device_id < self.device_num), \
                    f"Device id is out of the range [0, {self.device_num})."

        ret = acl.rt.set_context(self.context_dict[device_id])
        if ret != ACL_SUCCESS:
            raise ValueError(f"Set device {device_id} failed in func runmode, return {ret}.")

        run_mode, ret = acl.rt.get_run_mode()
        if ret != ACL_SUCCESS:
            raise ValueError(f"Get run mode of device {device_id} failed in \
                        func runmode, return {ret}.")

        return run_mode

    def current_context(self, devnum=None):
        if devnum in self.context_dict.keys():
            return self.context_dict[devnum]


    def bind_device(self, device_id):
        """bind device resource according to device_id.
            @note
            if the context of device_id is not exist, create a context and bind it.
        Args:
            device_id : device id.

        Returns:
            None.
        """
        if not isinstance(device_id, int):
            raise TypeError(f"Input device_id expects an int value, but got {type(device_id)}.")

        assert (device_id >= 0) and (device_id < self.device_num), \
                    f"Device id is out of the range [0, {self.device_num})."

        try:
            ret = acl.rt.set_context(self.context_dict[device_id])
            assert ret == ACL_SUCCESS, \
                f"Set context {self.context_dict[device_id]} failed, return {ret}." 
        except:
            ret = acl.rt.set_device(device_id)
            assert ret == ACL_SUCCESS, \
                f"Failed to set device {device_id} in func bind_device, return {ret}."

            context, ret = acl.rt.create_context(device_id)
            if ret != ACL_SUCCESS:
                raise ValueError(f"Create context failed on device {device_id}, return {ret}.")
            self.context_dict[device_id] = context

    def device_available(self):
        return (self.device_num > 0)

    def stream_add(self):
        pass

    def context_add(self):
        pass

    def __release_resource(self):
        """release device resource and deinitial.
        Args:
            None.

        Returns:
            None.
        """
        for device_id, ctx in self.context_dict.items():
            ret = acl.rt.destroy_context(ctx)
            if ret != ACL_SUCCESS:
                raise ValueError(f"Destroy context {ctx} failed in func \
                        __release_resource, return {ret}.")
       
            ret = acl.rt.reset_device(device_id)
            if ret != ACL_SUCCESS:
                raise ValueError(f"Reset device {device_id} failed in func \
                        __release_resource, return {ret}.")
        
        ret = acl.finalize()
        if ret != ACL_SUCCESS:
            raise ValueError(f"Finalize acl resource failed, return {ret}.")

    def __del__(self):
        self.__release_resource()


if __name__ == "__main__":
    acl_json = "./acl.json"
    resource = Context({0, 1}, acl_json)
    del resource
