# uploader.py
import os
import json
from config import VOD_SPACE_NAME
from vod_init import init_vod_service
from volcengine.util.Functions import Function
from volcengine.vod.models.request.request_vod_pb2 import VodUploadMediaRequest

def upload_video(file_path):
    """
    上传视频到火山云VOD
    :param file_path: 视频文件的路径
    :return: 上传结果
    """
    # 初始化VOD服务
    vod_service = init_vod_service()

    # 验证文件是否存在
    if not os.path.exists(file_path):
        return f"文件不存在: {file_path}"

    # 定义功能函数
    get_meta_function = Function.get_meta_func()
    snapshot_function = Function.get_snapshot_func(2.3)
    get_start_workflow_func = Function.get_start_workflow_template_func(
        [{"TemplateIds": ["imp template id"], "TemplateType": "imp"},
         {"TemplateIds": ["  template id"], "TemplateType": "transcode"}])
    apply_function = Function.get_add_option_info_func(title="米粉", classification_id=1731601509, tags="小米", description="小米米粉直播间", is_hls_index_only=True)

    try:
        # 创建上传请求
        req = VodUploadMediaRequest()
        req.SpaceName = VOD_SPACE_NAME
        req.FilePath = file_path
        req.Functions = json.dumps([get_meta_function, snapshot_function, get_start_workflow_func])
        req.CallbackArgs = ''
        req.FileName = os.path.basename(file_path)  # 自动提取文件名
        req.FileExtension = os.path.splitext(file_path)[-1]  # 自动提取文件扩展名
        req.StorageClass = 1
        req.UploadHostPrefer = ''

        # 上传视频
        resp = vod_service.upload_media(req)
    except Exception as e:
        return f"上传失败: {str(e)}"
    else:
        # 处理响应
        if resp.ResponseMetadata.Error.Code == '':
            return {
                "status": "success",
                "video_id": resp.Result.Data.Vid,
                "poster_uri": resp.Result.Data.PosterUri,
                "file_name": resp.Result.Data.SourceInfo.FileName,
                "height": resp.Result.Data.SourceInfo.Height,
                "width": resp.Result.Data.SourceInfo.Width
            }
        else:
            return {
                "status": "error",
                "error_code": resp.ResponseMetadata.Error.Code,
                "error_message": resp.ResponseMetadata.Error.Message
            }
