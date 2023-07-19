import boto3
import pytz
import logging
from datetime import datetime, timedelta

def get_all_images(repository_name):
    ecr_client = boto3.client('ecr')
    images = []

    # 获取第一页镜像
    response = ecr_client.list_images(repositoryName=repository_name, filter={'tagStatus': 'TAGGED'}, maxResults=1000)
    images.extend(response['imageIds'])

    # 检查是否有更多镜像
    while 'nextToken' in response:
        next_token = response['nextToken']

        # 获取下一页镜像
        response = ecr_client.list_images(repositoryName=repository_name, filter={'tagStatus': 'TAGGED'}, maxResults=1000, nextToken=next_token)
        images.extend(response['imageIds'])

    return images

def get_image_creation_time(ecr_client, repository_name, image_digest):
    response = ecr_client.describe_images(repositoryName=repository_name, imageIds=[{'imageDigest': image_digest}])
    image_details = response['imageDetails']
    if len(image_details) > 0:
        return image_details[0]['imagePushedAt']
    else:
        return None

def delete_images_batch(ecr_client, repository_name, image_tags):
    image_identifiers = [{'imageTag': tag} for tag in image_tags]
    response = ecr_client.batch_delete_image(repositoryName=repository_name, imageIds=image_identifiers)
    deleted_images = response['imageIds']
    deleted_tags = [image['imageTag'] for image in deleted_images]
    return deleted_tags

def delete_old_images(repository_name, days_to_retain, log_file, confirm_delete):
    # 配置日志
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    ecr_client = boto3.client('ecr')

    # 获取所有镜像
    all_images = get_all_images(repository_name)

    # 遍历每个镜像
    images_to_delete = []

    for image in all_images:
        image_tag = image['imageTag']
        image_digest = image['imageDigest']
        creation_time = get_image_creation_time(ecr_client, repository_name, image_digest)
        if not creation_time:
            continue

        # 将创建时间转换为带有时区信息的时间
        creation_time = creation_time.replace(tzinfo=pytz.UTC)

        retain_threshold = datetime.now(pytz.UTC) - timedelta(days=days_to_retain)
        if creation_time < retain_threshold:
            images_to_delete.append(image_tag)
            logging.info(f"Images to delete: {image_tag}")

    if images_to_delete:
        print(f"需要删除的镜像: {images_to_delete}")
        logging.info(f"Images to delete: {images_to_delete}")

        if confirm_delete:
            confirm = input("是否确认删除这些镜像？ (y/n): ")
            if confirm.lower() == 'y':
                # 将要删除的镜像分批进行删除操作
                batch_size = 100
                for i in range(0, len(images_to_delete), batch_size):
                    batch = images_to_delete[i:i+batch_size]
                    deleted_tags = delete_images_batch(ecr_client, repository_name, batch)
                    print(f"已删除镜像标签：{deleted_tags}")
                    logging.info(f"Deleted images with tags: {deleted_tags}")
            else:
                print("取消删除镜像。")
                logging.info("Cancelled image deletion.")
        else:
            # 将要删除的镜像分批进行删除操作
            batch_size = 100
            for i in range(0, len(images_to_delete), batch_size):
                batch = images_to_delete[i:i+batch_size]
                deleted_tags = delete_images_batch(ecr_client, repository_name, batch)
                print(f"已删除镜像标签：{deleted_tags}")
                logging.info(f"Deleted images with tags: {deleted_tags}")
    else:
        print("没有需要删除的镜像。")
        logging.info("No images to delete.")

# 配置参数
repository_name = 'ecr-middle-test'
days_to_retain = 90
log_file = 'clean_test.log'
confirm_delete = True   # 删除动作是否需要人为确认的开关，True表示需要确认，False表示默认同意删除

# 调用函数删除旧的镜像，开关confirm_delete设置为True
delete_old_images(repository_name, days_to_retain, log_file, confirm_delete)
