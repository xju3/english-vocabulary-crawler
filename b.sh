ffmpeg \
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/1.mp4'\
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/2.mp4'\
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/3.mp4'\
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/4.mp4'\
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/5.mp4'\
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/6.mp4'\
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/7.mp4'\
 -i '/Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/8.mp4'\
 -filter_complex "\
 [0:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v0];\
 [1:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v1];\
 [2:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v2];\
 [3:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v3];\
 [4:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v4];\
 [5:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v5];\
 [6:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v6];\
 [7:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v7];\
 [v0][0:a] [v1][1:a] [v2][2:a] [v3][3:a] [v4][4:a] [v5][5:a] [v6][6:a] [v7][7:a] concat=n=8:v=1:a=1[v][a]"\
 -map [v]\
 -map [a]\
 -vcodec\
 libx264\
 /Users/tju/Workspace/projects/english-vocabulary-crawler/tmp/122.C_eQDs0o8mf/122.mp4

