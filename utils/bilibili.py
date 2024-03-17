import hashlib
import os
import time
from bilibili_api import Credential
import httpx
from loguru import logger
import moviepy.editor as mp

cookies = {
    'buvid3': 'F9670C53-5139-A57B-5C7F-C280ED8E4A3341502infoc',
    'b_nut': '1708229941',
    'CURRENT_FNVAL': '4048',
    '_uuid': '175D372C-E388-10A72-103A3-F10813E1744B442381infoc',
    'buvid_fp': 'df6ab102a0b730211573395380988f24',
    'buvid4': '00CA9BFF-6C1F-F076-31E7-9D2E27BF74BD09869-024011307-Gr1Zs5Z0zVLAgOVXKZsVjJTnO1+iOyd46N7HcHg+5m7RDrPbsw9dxKXEM2Y4MaVL',
    'rpdid': '0zbfvRX90u|Y7ybcr1X|2dl|3w1RByDS',
    'enable_web_push': 'DISABLE',
    'header_theme_version': 'CLOSE',
    'bp_video_offset_3546561424394511': '891278852954783764',
    'PVID': '1',
    'bp_video_offset_102742156': '902763230400610324',
    'browser_resolution': '1270-854',
    'home_feed_column': '4',
    'FEED_LIVE_VERSION': 'V_SIDE_TO_FEED',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTAyMTQzNjQsImlhdCI6MTcwOTk1NTEwNCwicGx0IjotMX0.TEdc_skXtciZvMmOIDOKASUtkWvexJuHaFiBSk-yGCE',
    'bili_ticket_expires': '1710214304',
    'b_lsid': '81337B4E_18E216195C4',
    'SESSDATA': '839d1ad1%2C1725509409%2C76910%2A31CjAFpH3SN_vsh3etKZdgCTVKkCvqXKovmFQW8sQex2Ro6yYdYbi_ZAeCkFJsplZhFNASVm1SZTNSRmpDdmktTzdNMzJGQVVIVzlDQVlTTXg5dGtHdm5WaWhib0lyWTEzNFVhQTh4RzlIakREUm1XQkxhb2lKUkd0THJaNXN3T2hTUjhUcXFrMndBIIEC',
    'bili_jct': '4b38fff3c2697aa9e329abcc635be501',
    'DedeUserID': '102742156',
    'DedeUserID__ckMd5': '68d517f8697ef166',
    'sid': 'mn06wm2n',
}

credential = Credential.from_cookies(cookies)

from bilibili_api import video, sync, user, comment, session, HEADERS

FFMPEG_PATH = os.path.abspath('./ffmpeg.exe')


async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                f.write(chunk)




# 获取所有视频
async def get_all_videos(she, end_pn=10):
    init = list(range(1, end_pn + 1))
    all_videos = []
    # 如果失败了就重试
    for index, pn in enumerate(init):
        try:
            videos = await she.get_videos(0, pn, 30)
        except Exception as e:
            videos = []
            logger.error(f"{index} /{len(init)} -----> 页获取失败 直接记录了")
            time.sleep(10)
            init.append(pn)
            continue
        videos_meta = videos['list']['vlist']
        all_videos += videos_meta
        logger.success(f"{pn}  -----> {len(all_videos)}   获取陈工")
        time.sleep(5)
    return all_videos


# 获取视频播放链接--->提取音频
async def download_video_best(bvid, aid, local_filename):
    video_ele = video.Video(bvid=bvid, aid=aid, credential=credential)
    video_info = await video_ele.get_download_url(page_index=0)
    detecter = video.VideoDownloadURLDataDetecter(data=video_info)
    streams = detecter.detect_best_streams()
    if detecter.check_flv_stream() == True:
        flv_name = local_filename + ".flv"
        await download_url(streams[0].url, flv_name, "FLV 音视频流")
        os.system(f'{FFMPEG_PATH} -i {flv_name} {local_filename}')
        os.remove(flv_name)

    else:
        video_temp = local_filename + "video_temp.m4s"
        audio_temp = local_filename + "audio_temp.m4s"
        await download_url(streams[0].url, video_temp, "视频流")
        await download_url(streams[1].url, audio_temp, "音频流")

        os.system(f'{FFMPEG_PATH} -i {video_temp} -i {audio_temp} -vcodec copy  -acodec copy {local_filename} -y')
        os.remove(audio_temp)
        os.remove(video_temp)


def scale_and_crop_video(video_path, scaled_video_path, size_rate=1.2, watermark_text="永远热爱"):
    # 从中心出发 获取原本的宽高就是裁切啊
    video = mp.VideoFileClip(video_path)
    scaled_video = video.fx(mp.vfx.resize, size_rate)
    scaled_video = scaled_video.crop(x_center=scaled_video.w / 2, y_center=scaled_video.h / 2, width=video.w,
                                     height=video.h)

    # 添加文本水印
    txt_clip = (mp.TextClip(watermark_text, fontsize=24, color='white', print_cmd=True)
                .set_position((45,120))
                .set_duration(scaled_video.duration)
                .set_opacity(0.5))
    scaled_video = mp.CompositeVideoClip([scaled_video, txt_clip])

    scaled_video.write_videofile(scaled_video_path, threads=10)

    video.close()
    return scaled_video_path


# 同步获取视频列表 /////////////////////
def get_all_videos_sync(uid, end_pn=3):
    she = user.User(uid, credential=credential)
    all_videos = sync(get_all_videos(she, end_pn))
    return all_videos


def download_video_sync(bvid, aid, filename):
    try:
        video_info = sync(download_video_best(bvid, aid, filename))
        return video_info
    except Exception as e:
        return False


if __name__ == '__main__':
    # uid=27547211
    # all_videos=get_all_videos_sync(uid)
    # logger.success(f'获取视频成功    ---->   {all_videos}  ')

    # aid=1051375894
    # bvid='BV1sH4y1j7uX'

    # video_info=download_video_sync(bvid,aid)
    # logger.success(f'获取视频成功    ---->   {video_info}  ')

    last_mp4 = r"C:\projects\zhiqiang_hot\video.mp4"
    video_scaled_last_mp4 = r"C:\projects\zhiqiang_hot\video_scaled.mp4"

    scale_and_crop_video(last_mp4, video_scaled_last_mp4, 1.2)
