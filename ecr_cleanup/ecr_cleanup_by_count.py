import boto3
import logging
import re

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

def delete_old_images(repository_name, projects_file, retain_count, log_file, confirm_delete):
    # 配置日志
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    ecr_client = boto3.client('ecr')

    # 从文本文件读取项目列表
    with open(projects_file, 'r') as file:
        projects = [line.strip() for line in file]

    # 获取所有镜像
    all_images = get_all_images(repository_name)

    # 遍历每个项目
    for project in projects:
        logging.info(f"Processing project: {project}")

        # 过滤出当前项目的镜像标签
        filtered_tags = [image_tag['imageTag'] for image_tag in all_images if image_tag['imageTag'].startswith(project) and re.match(fr'{project}_\d+', image_tag['imageTag'])]

        # 对镜像标签进行排序，按照字符串的自然顺序
        sorted_tags = sorted(filtered_tags, key=lambda tag: [int(num) if num.isdigit() else num for num in re.split(r'(\d+)', tag)], reverse=True)

        print(f"{project} 总共发现镜像: {len(sorted_tags)}")
        logging.info(f"Total images found for project {project}: {len(sorted_tags)}")

        # 确认是否删除镜像
        if len(sorted_tags) > retain_count:
            images_to_delete = sorted_tags[retain_count:]
            print(f"{project} 需要删除的镜像: {images_to_delete}")
            logging.info(f"Images to delete for project {project}: {images_to_delete}")
            if confirm_delete:
                confirm = input("是否确认删除这些镜像？ (y/n): ")
                if confirm.lower() == 'y':
                    for image_tag in images_to_delete:
                        image_identifier = {'imageTag': image_tag}
                        ecr_client.batch_delete_image(repositoryName=repository_name, imageIds=[image_identifier])
                        print(f"已删除镜像标签：{image_tag}")
                        logging.info(f"Deleted image with tag: {image_tag}")

                else:
                    print("取消删除镜像。")
                    logging.info("Cancelled image deletion.")
            else:
                for image_tag in images_to_delete:
                    image_identifier = {'imageTag': image_tag}
                    ecr_client.batch_delete_image(repositoryName=repository_name, imageIds=[image_identifier])
                    print(f"已删除镜像标签：{image_tag}")
                    logging.info(f"Deleted image with tag: {image_tag}")
        else:
            print(f"{project}: 没有需要删除的镜像。")
            logging.info(f"{project}: No image to delete")

# 配置参数
repository_name = 'ecr-middle-dev'
projects_file = 'projects.txt'
retain_count = 2
log_file = 'clean_dev.log'
confirm_delete = True   # 删除动作是否需要人为确认的开关，True表示需要确认，False表示默认同意删除

# 调用函数删除旧的镜像，开关confirm_delete设置为True
delete_old_images(repository_name, projects_file, retain_count, log_file, confirm_delete)
