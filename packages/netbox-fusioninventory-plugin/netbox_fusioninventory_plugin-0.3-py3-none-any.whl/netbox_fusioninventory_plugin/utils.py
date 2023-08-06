import bs4
from dcim.models import *
from tenancy.models import *
from pprint import *
from django.utils.text import slugify

def created_or_update_device(device_dict):
    related_objects = [
            "manufacturer",
            "device_role",
            "tenant",
            "device_type",
            "platform",
            "site",
            "location",
            "rack",
            "face",
            "virtual_chassis",
            "vc_position",
            "vc_priority",
            "cluster",
        ]
    for key in related_objects:
        if device_dict[key]:
            if isinstance(device_dict[key], str):
                if key == "device_role":
                    device_dict[key] = DeviceRole.objects.get_or_create(
                            name = device_dict[key],
                            slug = slugify(device_dict[key]),
                            )[0]
                elif key == "manufacturer":
                    device_dict[key] = Manufacturer.objects.get_or_create(
                            name = device_dict[key],
                            slug = slugify(device_dict[key]),
                            )[0]
                elif key == "tenant":
                    device_dict[key] = Tenant.objects.get_or_create(
                            name = device_dict[key],
                            slug = slugify(device_dict[key]),
                            )[0]
                elif key == "device_type":
                    device_dict[key] = DeviceType.objects.get_or_create(
                            model = device_dict[key],
                            slug = slugify(device_dict[key]),
                            manufacturer = device_dict["manufacturer"]
                            )[0]
                    del device_dict["manufacturer"]
                elif key == "platform":
                    device_dict[key] = Platform.objects.get_or_create(
                            name = device_dict[key],
                            slug = slugify(device_dict[key]),
                            )[0]
                elif key == "site":
                    device_dict[key] = Site.objects.get_or_create(
                            name = device_dict[key],
                            slug = slugify(device_dict[key]),
                            )[0]
                elif key == "location":
                    device_dict[key] = Location.objects.get_or_create(
                            name = device_dict[key],
                            slug = slugify(device_dict[key]),
                            )[0]
                elif key == "rack":
                    device_dict[key] = Rack.objects.get_or_create(
                            name = device_dict[key],
                            slug = slugify(device_dict[key]),
                            )[0]
        else:
            del device_dict[key]
    to_del = []
    for k,v in device_dict.items():
        if not v:
            to_del.append(k)
    for key in to_del:
        del device_dict[key]
    pprint(device_dict)
    Device.objects.update_or_create(**device_dict)


def soup_to_dict(soup, config):
    default_config = {
            "name":"xml:request.content.hardware.name",
            "device_role":"object:DeviceRole:unknow",
            "tenant":None,
            "manufacturer":"xml:request.content.bios.mmanufacturer",
            "device_type":"xml:request.content.bios.mmodel",
            "platform":"xml:request.content.hardware.osname",
            "serial":"xml:request.content.bios.msn",
            "asset_tag":"xml:request.content.bios.assettag",
            "status":"str:active",
            "site":"object:Site:unknow",
            "location":None,
            "rack":None,
            "position":None,
            "face":None,
            "virtual_chassis":None,
            "vc_position":None,
            "vc_priority":None,
            "cluster":None,
            "comments":None,
            }
    build_config = default_config
    result = {}
    for k,v in default_config.items():
        if k in config:
            build_config[k] = config[k]
        else:
            build_config[k] = v
    for k,v in build_config.items():
        if v:
            value_type, content = v.split(':',1)
            if value_type == "xml":
                path, tag = content.rsplit('.',1)
                result[k] = eval("soup." + path + '.find("' + tag + '").get_text()')
            elif value_type == "object":
                obj_type, value = content.split(':',1)
                if value.isdigit():
                    result[k] = eval(obj_type + ".objects.filter(id=" + value + ")[0]")
                else:
                    result[k] = eval(obj_type + ".objects.get_or_create(name='" + value + "', slug=slugify('" + value + "'))")[0]
        else:
            result[k] = v
    return result
