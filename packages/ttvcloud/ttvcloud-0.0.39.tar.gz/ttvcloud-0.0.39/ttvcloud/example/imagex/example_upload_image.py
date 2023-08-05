# coding:utf-8
from __future__ import print_function
import requests
from ttvcloud.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    imagex_service.set_ak('AKLTMDRhMGQ1ZWE4NjZkNDg0ZGJmMjg5OTUzNzU4NzRmOWM')
    imagex_service.set_sk('u4zCNZS9bFjqNjaazTASYgkNUfk9vM/i2rp8zXzTjHN64YoU+/wx+iJfZv5LUt9B')

    service_id = 'su4pp6x6rv'
    file_paths = ['/Users/fuye/Downloads/4321.txt']

    # resp = imagex_service.upload_image(service_id, file_paths)
    # print(resp)

    response = requests.request("GET", "http://tosv.byted.org/obj/imagex-rc/1.png")
    img_datas = []
    img_datas.append(response.text)
    resp = imagex_service.upload_image_data(service_id, img_datas)
    print(resp)
