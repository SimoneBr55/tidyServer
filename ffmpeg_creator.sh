#!/bin/bash

source .set_env_vars

# Removing old videos...
rm $dailyphoto_mp4
rm $dailyvideo_mp4

# FFMPEG create videos

ffmpeg -f concat -safe 0 -i $img_ffmpeg_txt -b:v 1M -vf fps=10 -pix_fmt yuv420p /tmp/output_img.mp4

mv /tmp/output_img.mp4 $dailyphoto_mp4

ffmpeg -f concat -safe 0 -i $vid_ffmpeg_txt -b:v 1M -vf fps=10 -pix_fmt yuv420p /tmp/output_vid.mp4

mv /tmp/output_vid.mp4 $dailyvideo_mp4
