import math #line:2
from scipy import signal #line:3
from copy import deepcopy #line:4
import numpy as np #line:5
import cv2 #line:6
import pickle #line:7
from vcopt import vcopt #line:8
try :#line:10
    from foot_tool import ft ,pl_class ,cl_class #line:11
    print ('import normal version')#line:12
except :#line:13
    from .foot_tool import ft ,pl_class ,cl_class #line:14
    print ('import . version')#line:15
class vcfoot :#line:20
    def __init__ (OO00OO000OO00OO00 ):#line:21
        pass #line:22
    def __del__ (O000OOOO0000OOOOO ):#line:23
        pass #line:24
    def level (O0O0OO0O00O0O0OO0 ,O0OO0OOO00OO00OO0 ,url =None ,flip =False ,save =None ,test =0 ):#line:27
        print ('\n### objファイルの読み込み')#line:29
        OO0OOO00OOOO000O0 ,OO0000000000OO000 ,O0OO0OO00OOO0O0O0 =ft .load_obj (O0OO0OOO00OO00OO0 )#line:31
        if np .max (OO0000000000OO000 )<=1.0 :#line:33
            OO0000000000OO000 =np .array (OO0000000000OO000 *255.0 ,int )#line:34
        OO0O00O0000O00000 ,OOO0OO000000OO00O =ft .down_sample (OO0OOO00OOOO000O0 ,OO0000000000OO000 ,20000 )#line:36
        if test :#line:37
            ft .showc (OO0O00O0000O00000 ,OOO0OO000000OO00O ,'xz')#line:38
        print ('\n### 静置GA')#line:44
        try :#line:46
            O00OOO0OOOOO0O000 #line:47
        except NameError :#line:48
            print ('\n### ダウンサンプル')#line:50
            OO0O00O0000O00000 ,OOO0OO000000OO00O =ft .down_sample (OO0OOO00OOOO000O0 ,OO0000000000OO000 ,8000 )#line:52
            def O000O00O0OO00O000 (OOOOOOOO00O00OO00 ):#line:55
                O0OO0OO0OOO00O0O0 =deepcopy (OO0O00O0000O00000 )#line:57
                O0OO0OO0OOO00O0O0 =ft .rotate_3D_x (O0OO0OO0OOO00O0O0 ,OOOOOOOO00O00OO00 [0 ])#line:58
                O0OO0OO0OOO00O0O0 =ft .rotate_3D_y (O0OO0OO0OOO00O0O0 ,OOOOOOOO00O00OO00 [1 ])#line:59
                OOOOOOOOO0O000OOO ,O0OO0OOO00O0OO00O =np .histogram (O0OO0OO0OOO00O0O0 [:,2 ],bins =50 )#line:61
                OOOO00000O0O0OOO0 =4 #line:63
                O0O0OOO00OO0OO0O0 =np .ones (OOOO00000O0O0OOO0 )/OOOO00000O0O0OOO0 #line:64
                OOO000O00OO0O0O0O =signal .convolve (OOOOOOOOO0O000OOO ,O0O0OOO00OO0OO0O0 ,mode ='same')#line:65
                O0OO0O00OO0000OO0 =np .max (OOO000O00OO0O0O0O )#line:67
                return O0OO0O00OO0000OO0 #line:68
            def O0OO00OOO00O00O00 ():#line:71
                O0O0O0O0OOO0OO000 =[[0 ,180 ],[0 ,180 ]]#line:73
                OOOO0O0O0OO00OO00 ,O0O0O000OO00O0O00 =vcopt ().rcGA (O0O0O0O0OOO0OO000 ,O000O00O0OO00O000 ,99999 ,show_pool_func ='bar',seed ='grendel_master_eternity',pool_num =100 ,core_num =8 ,max_gen =10000 )#line:82
                return OOOO0O0O0OO00OO00 #line:83
            print ('\n### 静置GA')#line:86
            O00OOO0OOOOO0O000 =O0OO00OOO00O00O00 ()#line:88
            print ('para = [{}, {}]'.format (O00OOO0OOOOO0O000 [0 ],O00OOO0OOOOO0O000 [1 ]))#line:90
        print ('\n### 反映')#line:94
        OO0OOO00OOOO000O0 =ft .rotate_3D_x (OO0OOO00OOOO000O0 ,O00OOO0OOOOO0O000 [0 ])#line:96
        OO0OOO00OOOO000O0 =ft .rotate_3D_y (OO0OOO00OOOO000O0 ,O00OOO0OOOOO0O000 [1 ])#line:97
        print ('\n### 確認')#line:102
        OO0O00O0000O00000 ,OOO0OO000000OO00O =ft .down_sample (OO0OOO00OOOO000O0 ,OO0000000000OO000 ,20000 )#line:104
        if test :#line:105
            ft .showc (OO0O00O0000O00000 ,OOO0OO000000OO00O ,'xz')#line:106
        print ('\n### 逆さなら反転')#line:118
        OOOOO00OO000O0000 =np .median (OO0OOO00OOOO000O0 [:,2 ])#line:121
        O0O0O00O000O00000 =np .mean (OO0OOO00OOOO000O0 [:,2 ])#line:122
        OOO00O00OO00OO0O0 =O0O0O00O000O00000 >OOOOO00OO000O0000 #line:123
        print ('up_bool:\n{}'.format (OOO00O00OO00OO0O0 ))#line:124
        if OOO00O00OO00OO0O0 ==True :#line:126
            if flip ==False :#line:128
                pass #line:129
            if flip ==True :#line:131
                print ('強制反転')#line:132
                OO0OOO00OOOO000O0 =ft .rotate_3D_x (OO0OOO00OOOO000O0 ,180 )#line:133
        else :#line:135
            if flip ==False :#line:137
                print ('通常反転')#line:138
                OO0OOO00OOOO000O0 =ft .rotate_3D_x (OO0OOO00OOOO000O0 ,180 )#line:139
            if flip ==True :#line:142
                pass #line:143
        print ('\n### 確認')#line:146
        OO0O00O0000O00000 ,OOO0OO000000OO00O =ft .down_sample (OO0OOO00OOOO000O0 ,OO0000000000OO000 ,20000 )#line:148
        if test :#line:149
            ft .showc (OO0O00O0000O00000 ,OOO0OO000000OO00O ,'xz')#line:150
        print ('\n### zレベル補正')#line:155
        O0OO0OOOOOO000000 ,OO0OOO00OOOO00O0O =np .histogram (OO0OOO00OOOO000O0 [:,2 ],bins =100 )#line:158
        OO000O0OO00O0O0OO =4 #line:160
        OOO0000OO0O0OO0OO =np .ones (OO000O0OO00O0O0OO )/OO000O0OO00O0O0OO #line:161
        O000OO00O00OO0OO0 =signal .convolve (O0OO0OOOOOO000000 ,OOO0000OO0O0OO0OO ,mode ='same')#line:162
        O0O0O00OOOO0O000O =OO0OOO00OOOO00O0O [np .argmax (O000OO00O00OO0OO0 )]#line:164
        print ('z_level:\n{}'.format (O0O0O00OOOO0O000O ))#line:165
        OO0OOO00OOOO000O0 [:,2 ]-=O0O0O00OOOO0O000O #line:167
        OO0OOO00OOOO000O0 [:,0 ]-=np .min (OO0OOO00OOOO000O0 [:,0 ])#line:170
        OO0OOO00OOOO000O0 [:,1 ]-=np .min (OO0OOO00OOOO000O0 [:,1 ])#line:171
        print ('\n### 確認')#line:174
        OO0O00O0000O00000 ,OOO0OO000000OO00O =ft .down_sample (OO0OOO00OOOO000O0 ,OO0000000000OO000 ,20000 )#line:176
        if test :#line:177
            ft .showc (OO0O00O0000O00000 ,OOO0OO000000OO00O ,'xz')#line:178
        if save !=None :#line:180
            print ('\n### 保存')#line:182
            with open (save ,'wb')as O0O00000000O00OOO :#line:184
                pickle .dump ([OO0OOO00OOOO000O0 ,OO0000000000OO000 ,O0OO0OO00OOO0O0O0 ],O0O00000000O00OOO )#line:185
            ft .showc (OO0O00O0000O00000 ,OOO0OO000000OO00O ,'xz',save =save +'.png')#line:186
    def enkaku (OO00OOOOOO0O0000O ,O0O0OOO0O0O0O00O0 ,paper_long =297 ,paper_short =210 ,window_size =900 ,dot_size =1 ,cut_height =90 ,rate1 =0.18 ,rate2 =0.44 ,rate3 =0.54 ,test =0 ):#line:209
        print ('\n### pcklファイルの読み込み')#line:247
        if O0O0OOO0O0O0O00O0 [:4 ]=='http':#line:250
            OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,OO00O000OOO0OOO00 =ft .load_pckl_url (O0O0OOO0O0O0O00O0 )#line:251
        else :#line:252
            OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,OO00O000OOO0OOO00 =ft .load_pckl (O0O0OOO0O0O0O00O0 )#line:253
        if np .max (O0O0OO000OOOOO0OO )<=1.0 :#line:255
            O0O0OO000OOOOO0OO =np .array (O0O0OO000OOOOO0OO *255.0 ,int )#line:256
        OO00O000OOO0OOO00 -=1 #line:259
        OO0O0O00O0000OOO0 =OOOOOOO00000O00OO [OO00O000OOO0OOO00 ]#line:260
        O00000O00O0O0O0O0 =O0O0OO000OOOOO0OO [OO00O000OOO0OOO00 ]#line:262
        if test :#line:265
            OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,20000 )#line:266
            ft .showc (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,'xy')#line:267
        print ('\n### 紙の大きさにカット')#line:273
        try :#line:275
            O0000OOOO00O0OO0O #line:276
            OO0OOOOOO00O0OO0O #line:277
        except NameError :#line:278
            print ('\n### 前処理')#line:280
            OOO00OOOO0OO000OO =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:283
            OO0O00O00O0O00O0O ,OO00O0O0OO0OO0O0O =OOO00OOOO0OO000OO .window_zoom (OO0O0O00O0000OOO0 ,O00000O00O0O0O0O0 )#line:285
            OO0O00O00O0O00O0O =OOO00OOOO0OO000OO .put_text (OO0O00O00O0O00O0O ,['1, Center of paper','2, Select cut range (about)'])#line:288
            O0OO0000OO0OOO00O ='step1'#line:297
            cv2 .namedWindow (O0OO0000OO0OOO00O )#line:298
            O00O0OO000OOOO00O =2 #line:299
            O00000OO0OO0OOO00 =pl_class (O00O0OO000OOOO00O )#line:300
            cv2 .setMouseCallback (O0OO0000OO0OOO00O ,OOO00OOOO0OO000OO .onMouse ,[O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O ,O00000OO0OO0OOO00 ])#line:301
            cv2 .imshow (O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O )#line:302
            cv2 .waitKey ()#line:303
            print ('\n### 後処理')#line:306
            O0000OOOO00O0OO0O =np .array (OOO00OOOO0OO000OO .p [0 ],float )#line:309
            OO0OOOOOO00O0OO0O =max (abs (OOO00OOOO0OO000OO .p [1 ,0 ]-OOO00OOOO0OO000OO .p [0 ,0 ]),abs (OOO00OOOO0OO000OO .p [1 ,1 ]-OOO00OOOO0OO000OO .p [0 ,1 ]))#line:310
            O0000OOOO00O0OO0O =O0000OOOO00O0OO0O /OO00O0O0OO0OO0O0O #line:313
            OO0OOOOOO00O0OO0O =OO0OOOOOO00O0OO0O /OO00O0O0OO0OO0O0O #line:314
            print ('cut_center = [{}, {}]'.format (O0000OOOO00O0OO0O [0 ],O0000OOOO00O0OO0O [1 ]))#line:315
            print ('cut_len = {}'.format (OO0OOOOOO00O0OO0O ))#line:316
        print ('\n### 反映')#line:320
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,0 ]>O0000OOOO00O0OO0O [1 ]-OO0OOOOOO00O0OO0O ]#line:323
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,0 ]>O0000OOOO00O0OO0O [1 ]-OO0OOOOOO00O0OO0O ]#line:324
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,0 ]<O0000OOOO00O0OO0O [1 ]+OO0OOOOOO00O0OO0O ]#line:325
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,0 ]<O0000OOOO00O0OO0O [1 ]+OO0OOOOOO00O0OO0O ]#line:326
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,1 ]>O0000OOOO00O0OO0O [0 ]-OO0OOOOOO00O0OO0O ]#line:328
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,1 ]>O0000OOOO00O0OO0O [0 ]-OO0OOOOOO00O0OO0O ]#line:329
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,1 ]<O0000OOOO00O0OO0O [0 ]+OO0OOOOOO00O0OO0O ]#line:330
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,1 ]<O0000OOOO00O0OO0O [0 ]+OO0OOOOOO00O0OO0O ]#line:331
        OOO000OOO0O0OO0O0 =OO0O0O00O0000OOO0 [:,:,0 ]>O0000OOOO00O0OO0O [1 ]-OO0OOOOOO00O0OO0O #line:333
        O000OO00O0OOOO0OO =OO0O0O00O0000OOO0 [:,:,0 ]<O0000OOOO00O0OO0O [1 ]+OO0OOOOOO00O0OO0O #line:334
        O000OOO00OOO00OOO =OO0O0O00O0000OOO0 [:,:,1 ]>O0000OOOO00O0OO0O [0 ]-OO0OOOOOO00O0OO0O #line:335
        O000OO0000O0O0OO0 =OO0O0O00O0000OOO0 [:,:,1 ]<O0000OOOO00O0OO0O [0 ]+OO0OOOOOO00O0OO0O #line:336
        O00OO0O00OOO0O0O0 =OOO000OOO0O0OO0O0 *O000OO00O0OOOO0OO *O000OOO00OOO00OOO *O000OO0000O0O0OO0 #line:337
        O00OO0O00OOO0O0O0 =np .sum (O00OO0O00OOO0O0O0 ,axis =1 )#line:338
        OO0O0O00O0000OOO0 =OO0O0O00O0000OOO0 [O00OO0O00OOO0O0O0 ==3 ]#line:339
        O00000O00O0O0O0O0 =O00000O00O0O0O0O0 [O00OO0O00OOO0O0O0 ==3 ]#line:340
        print (OO0O0O00O0000OOO0 .shape )#line:341
        OO0O0O00O0000OOO0 [:,:,0 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:345
        OO0O0O00O0000OOO0 [:,:,1 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:346
        OOOOOOO00000O00OO [:,0 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:347
        OOOOOOO00000O00OO [:,1 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:348
        print ('\n### 確認')#line:351
        OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,20000 )#line:353
        if test :#line:355
            ft .showc (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,'xy')#line:356
        print ('\n### 紙のサイズ校正')#line:368
        try :#line:370
            O00O00O0OOOO000O0 #line:371
            O0O0OOO0000O0O0OO #line:372
            O00O00OO00O0000OO #line:373
        except NameError :#line:374
            print ('\n### 前処理')#line:376
            OOO00OOOO0OO000OO =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:379
            OO0O00O00O0O00O0O ,OO00O0O0OO0OO0O0O =OOO00OOOO0OO000OO .window_zoom (OO0O0O00O0000OOO0 ,O00000O00O0O0O0O0 )#line:381
            OO0O00O00O0O00O0O =OOO00OOOO0OO000OO .put_text (OO0O00O00O0O00O0O ,['1, Top-left of paper','2, Bottom-right of paper'])#line:384
            O0OO0000OO0OOO00O ='step2'#line:390
            cv2 .namedWindow (O0OO0000OO0OOO00O )#line:391
            O00O0OO000OOOO00O =2 #line:392
            O00000OO0OO0OOO00 =pl_class (O00O0OO000OOOO00O )#line:393
            cv2 .setMouseCallback (O0OO0000OO0OOO00O ,OOO00OOOO0OO000OO .onMouse ,[O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O ,O00000OO0OO0OOO00 ])#line:394
            cv2 .imshow (O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O )#line:395
            cv2 .waitKey ()#line:396
            print ('\n### 後処理')#line:399
            O0O0OOO0000O0O0OO =np .array (OOO00OOOO0OO000OO .p [0 ],float )/OO00O0O0OO0OO0O0O #line:402
            print ('top_left = [{}, {}]'.format (O0O0OOO0000O0O0OO [0 ],O0O0OOO0000O0O0OO [1 ]))#line:403
            O00O00OO00O0000OO =np .array (OOO00OOOO0OO000OO .p [1 ],float )/OO00O0O0OO0OO0O0O #line:406
            print ('bottom_right = [{}, {}]'.format (O00O00OO00O0000OO [0 ],O00O00OO00O0000OO [1 ]))#line:407
            OOOOO0OO000O00O00 =math .atan2 (O00O00OO00O0000OO [1 ]-O0O0OOO0000O0O0OO [1 ],O00O00OO00O0000OO [0 ]-O0O0OOO0000O0O0OO [0 ])#line:410
            OO0O000O0000O00O0 =math .degrees (OOOOO0OO000O00O00 )#line:412
            O0OOOO00O00O00OOO =math .atan2 (paper_long ,paper_short )#line:416
            O00O0O0OO0OOO0000 =math .degrees (O0OOOO00O00O00OOO )#line:418
            O00O00O0OOOO000O0 =O00O0O0OO0OOO0000 -OO0O000O0000O00O0 #line:422
            if O00O00O0OOOO000O0 >180 :#line:423
                O00O00O0OOOO000O0 =-360 +O00O00O0OOOO000O0 #line:424
            if O00O00O0OOOO000O0 <-180 :#line:425
                O00O00O0OOOO000O0 =360 -O00O00O0OOOO000O0 #line:426
            print ('rotation_paper = {}'.format (O00O00O0OOOO000O0 ))#line:427
        print ('\n### 反映')#line:431
        O0O0OOO0000O0O0OO =ft .rotate_2D_z (O0O0OOO0000O0O0OO ,theta =-O00O00O0OOOO000O0 )#line:434
        O00O00OO00O0000OO =ft .rotate_2D_z (O00O00OO00O0000OO ,theta =-O00O00O0OOOO000O0 )#line:435
        OOOOOOO00000O00OO =ft .rotate_3D_z (OOOOOOO00000O00OO ,theta =-O00O00O0OOOO000O0 )#line:436
        for O00O0O0O00OO00O0O in range (3 ):#line:437
            OO0O0O00O0000OOO0 [:,O00O0O0O00OO00O0O ,:]=ft .rotate_3D_z (OO0O0O00O0000OOO0 [:,O00O0O0O00OO00O0O ,:],theta =-O00O00O0OOOO000O0 )#line:438
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,0 ]>O0O0OOO0000O0O0OO [1 ]]#line:441
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,0 ]>O0O0OOO0000O0O0OO [1 ]]#line:442
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,0 ]<O00O00OO00O0000OO [1 ]]#line:443
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,0 ]<O00O00OO00O0000OO [1 ]]#line:444
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,1 ]>O0O0OOO0000O0O0OO [0 ]]#line:446
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,1 ]>O0O0OOO0000O0O0OO [0 ]]#line:447
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,1 ]<O00O00OO00O0000OO [0 ]]#line:448
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,1 ]<O00O00OO00O0000OO [0 ]]#line:449
        OOO000OOO0O0OO0O0 =OO0O0O00O0000OOO0 [:,:,0 ]>O0O0OOO0000O0O0OO [1 ]#line:451
        O000OO00O0OOOO0OO =OO0O0O00O0000OOO0 [:,:,0 ]<O00O00OO00O0000OO [1 ]#line:452
        O000OOO00OOO00OOO =OO0O0O00O0000OOO0 [:,:,1 ]>O0O0OOO0000O0O0OO [0 ]#line:453
        O000OO0000O0O0OO0 =OO0O0O00O0000OOO0 [:,:,1 ]<O00O00OO00O0000OO [0 ]#line:454
        O00OO0O00OOO0O0O0 =OOO000OOO0O0OO0O0 *O000OO00O0OOOO0OO *O000OOO00OOO00OOO *O000OO0000O0O0OO0 #line:455
        O00OO0O00OOO0O0O0 =np .sum (O00OO0O00OOO0O0O0 ,axis =1 )#line:456
        OO0O0O00O0000OOO0 =OO0O0O00O0000OOO0 [O00OO0O00OOO0O0O0 ==3 ]#line:457
        O00000O00O0O0O0O0 =O00000O00O0O0O0O0 [O00OO0O00OOO0O0O0 ==3 ]#line:458
        print (OO0O0O00O0000OOO0 .shape )#line:459
        OO0O00O0O00OO0OOO =O00O00OO00O0000OO [0 ]-O0O0OOO0000O0O0OO [0 ]#line:463
        O00000O0O0OO000O0 =O00O00OO00O0000OO [1 ]-O0O0OOO0000O0O0OO [1 ]#line:464
        O0O000OO0O00O0O0O =paper_short /OO0O00O0O00OO0OOO #line:466
        OO0OOOO0OOO0OO00O =paper_long /O00000O0O0OO000O0 #line:467
        OO00O0O0OO0OO0O0O =(O0O000OO0O00O0O0O +OO0OOOO0OOO0OO00O )/2 #line:471
        O0O0OOO0000O0O0OO *=OO00O0O0OO0OO0O0O #line:474
        O00O00OO00O0000OO *=OO00O0O0OO0OO0O0O #line:475
        OOOOOOO00000O00OO *=OO00O0O0OO0OO0O0O #line:476
        OO0O0O00O0000OOO0 *=OO00O0O0OO0OO0O0O #line:477
        O0O0OO000OOOOO0OO =O0O0OO000OOOOO0OO [OOOOOOO00000O00OO [:,2 ]<cut_height ]#line:480
        OOOOOOO00000O00OO =OOOOOOO00000O00OO [OOOOOOO00000O00OO [:,2 ]<cut_height ]#line:481
        O00OO0O00OOO0O0O0 =OO0O0O00O0000OOO0 [:,:,2 ]<cut_height #line:483
        print (O00OO0O00OOO0O0O0 .shape )#line:484
        O00OO0O00OOO0O0O0 =np .sum (O00OO0O00OOO0O0O0 ,axis =1 )#line:485
        OO0O0O00O0000OOO0 =OO0O0O00O0000OOO0 [O00OO0O00OOO0O0O0 ==3 ]#line:486
        O00000O00O0O0O0O0 =O00000O00O0O0O0O0 [O00OO0O00OOO0O0O0 ==3 ]#line:487
        print (OO0O0O00O0000OOO0 .shape )#line:488
        O0O0OOO0000O0O0OO [1 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:491
        O0O0OOO0000O0O0OO [0 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:492
        O00O00OO00O0000OO [1 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:493
        O00O00OO00O0000OO [0 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:494
        OO0O0O00O0000OOO0 [:,:,0 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:495
        OO0O0O00O0000OOO0 [:,:,1 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:496
        OOOOOOO00000O00OO [:,0 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:497
        OOOOOOO00000O00OO [:,1 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:498
        print ('\n### 確認')#line:502
        OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,20000 )#line:504
        if test :#line:505
            ft .showc (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,'xy',O0O0OOO0000O0O0OO ,O00O00OO00O0000OO )#line:506
        print ('\n### 足の向き補正')#line:524
        try :#line:526
            OOO00OOO0O00OO0O0 #line:527
            O0O00O0O0O0O0OO0O #line:528
            OO0OOOO0OO0O0O0OO #line:529
        except NameError :#line:530
            print ('\n### 前処理')#line:532
            OOO00OOOO0OO000OO =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:535
            OO0O00O00O0O00O0O ,OO00O0O0OO0OO0O0O =OOO00OOOO0OO000OO .window_zoom (OO0O0O00O0000OOO0 ,O00000O00O0O0O0O0 )#line:537
            OO0O00O00O0O00O0O =OOO00OOOO0OO000OO .put_text (OO0O00O00O0O00O0O ,['1, Second-finger tip','2, Heel tip'],right =True )#line:540
            O0OO0000OO0OOO00O ='step3'#line:546
            cv2 .namedWindow (O0OO0000OO0OOO00O )#line:547
            O00O0OO000OOOO00O =2 #line:548
            O00000OO0OO0OOO00 =pl_class (O00O0OO000OOOO00O )#line:549
            cv2 .setMouseCallback (O0OO0000OO0OOO00O ,OOO00OOOO0OO000OO .onMouse ,[O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O ,O00000OO0OO0OOO00 ])#line:550
            cv2 .imshow (O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O )#line:551
            cv2 .waitKey ()#line:552
            print ('\n### 後処理')#line:555
            OOO00OOO0O00OO0O0 =np .array (OOO00OOOO0OO000OO .p [0 ],float )/OO00O0O0OO0OO0O0O #line:558
            print ('foot_tip = [{}, {}]'.format (OOO00OOO0O00OO0O0 [0 ],OOO00OOO0O00OO0O0 [1 ]))#line:559
            O0O00O0O0O0O0OO0O =np .array (OOO00OOOO0OO000OO .p [1 ],float )/OO00O0O0OO0OO0O0O #line:562
            print ('heel_tip = [{}, {}]'.format (O0O00O0O0O0O0OO0O [0 ],O0O00O0O0O0O0OO0O [1 ]))#line:563
            OOOOO0OO000O00O00 =math .atan2 (O0O00O0O0O0O0OO0O [1 ]-OOO00OOO0O00OO0O0 [1 ],O0O00O0O0O0O0OO0O [0 ]-OOO00OOO0O00OO0O0 [0 ])#line:566
            OO0O000O0000O00O0 =math .degrees (OOOOO0OO000O00O00 )#line:567
            OO0OOOO0OO0O0O0OO =OO0O000O0000O00O0 -90 #line:569
            if OO0OOOO0OO0O0O0OO >180 :#line:571
                OO0OOOO0OO0O0O0OO =-360 +OO0OOOO0OO0O0O0OO #line:572
            if OO0OOOO0OO0O0O0OO <-180 :#line:573
                OO0OOOO0OO0O0O0OO =360 -OO0OOOO0OO0O0O0OO #line:574
            print ('rotation_foot = {}'.format (OO0OOOO0OO0O0O0OO ))#line:575
        print ('\n### 反映')#line:579
        OOO00OOO0O00OO0O0 =ft .rotate_2D_z (OOO00OOO0O00OO0O0 ,theta =OO0OOOO0OO0O0O0OO )#line:582
        O0O00O0O0O0O0OO0O =ft .rotate_2D_z (O0O00O0O0O0O0OO0O ,theta =OO0OOOO0OO0O0O0OO )#line:583
        OOOOOOO00000O00OO =ft .rotate_3D_z (OOOOOOO00000O00OO ,theta =OO0OOOO0OO0O0O0OO )#line:584
        for O00O0O0O00OO00O0O in range (3 ):#line:585
            OO0O0O00O0000OOO0 [:,O00O0O0O00OO00O0O ,:]=ft .rotate_3D_z (OO0O0O00O0000OOO0 [:,O00O0O0O00OO00O0O ,:],theta =OO0OOOO0OO0O0O0OO )#line:586
        OOO00OOO0O00OO0O0 [1 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:590
        OOO00OOO0O00OO0O0 [0 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:591
        O0O00O0O0O0O0OO0O [1 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:592
        O0O00O0O0O0O0OO0O [0 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:593
        OO0O0O00O0000OOO0 [:,:,0 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:594
        OO0O0O00O0000OOO0 [:,:,1 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:595
        OOOOOOO00000O00OO [:,0 ]-=np .min (OOOOOOO00000O00OO [:,0 ])#line:596
        OOOOOOO00000O00OO [:,1 ]-=np .min (OOOOOOO00000O00OO [:,1 ])#line:597
        print ('\n### 確認')#line:601
        OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,20000 )#line:603
        if test :#line:604
            ft .showc (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,'xy',OOO00OOO0O00OO0O0 ,O0O00O0O0O0O0OO0O )#line:605
        print ('\n### 足の測定１')#line:624
        try :#line:626
            OO0O00O0O0O0O000O #line:627
            O0O00O0OO000OOOO0 #line:628
            O00O0OO000O000OO0 #line:629
            OOOOO00O0O000OOO0 #line:630
            O0OOOOO000OOO0OOO #line:631
            O00OO00OOO00O0OO0 #line:632
            OO000O00O0O0000OO #line:633
            OO0OOOO0O00OOO00O #line:634
            O000OOOO00OOO00O0 #line:635
        except NameError :#line:636
            print ('\n### 前処理')#line:638
            OOO00OOOO0OO000OO =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:641
            OO0O00O00O0O00O0O ,OO00O0O0OO0OO0O0O =OOO00OOOO0OO000OO .window_zoom (OO0O0O00O0000OOO0 ,O00000O00O0O0O0O0 )#line:643
            OO0O00O00O0O00O0O =OOO00OOOO0OO000OO .put_text (OO0O00O00O0O00O0O ,['1, Toe tip','2, Heel tip','3, Heel-left','4, Heel-right','5, Width-left','6, Width-right'],right =True )#line:650
            O0OO0000OO0OOO00O ='step4'#line:656
            cv2 .namedWindow (O0OO0000OO0OOO00O )#line:657
            O00O0OO000OOOO00O =6 #line:658
            O00000OO0OO0OOO00 =pl_class (O00O0OO000OOOO00O )#line:659
            cv2 .setMouseCallback (O0OO0000OO0OOO00O ,OOO00OOOO0OO000OO .onMouse ,[O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O ,O00000OO0OO0OOO00 ])#line:660
            cv2 .imshow (O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O )#line:661
            cv2 .waitKey ()#line:662
            print ('\n### 後処理')#line:665
            O0OOO000O0O0OO00O ,O00OO0O0O0O0000OO =OOO00OOOO0OO000OO .p [0 ]/OO00O0O0OO0OO0O0O #line:668
            O0O0O000OO0O00OOO ,OO0O0O0000OO0O0O0 =OOO00OOOO0OO000OO .p [1 ]/OO00O0O0OO0OO0O0O #line:669
            OOOOO00OOOO0OOOO0 ,OOOOO000OOO00OO00 =OOO00OOOO0OO000OO .p [2 ]/OO00O0O0OO0OO0O0O #line:670
            OO0OO000OO00000OO ,O0O0000O00O0O00OO =OOO00OOOO0OO000OO .p [3 ]/OO00O0O0OO0OO0O0O #line:671
            OOO0O0OO00OOO00OO ,O0O0O0OOO0OOOO0OO =OOO00OOOO0OO000OO .p [4 ]/OO00O0O0OO0OO0O0O #line:672
            O0O0000OOOOOO0OOO ,O0OO0OO00OO0O00OO =OOO00OOOO0OO000OO .p [5 ]/OO00O0O0OO0OO0O0O #line:673
            OO0O00O0O0O0O000O =abs (OO0O0O0000OO0O0O0 -O00OO0O0O0O0000OO )#line:676
            print ('l_foot = {}'.format (OO0O00O0O0O0O000O ))#line:677
            O0O00O0OO000OOOO0 =abs (OO0OO000OO00000OO -OOOOO00OOOO0OOOO0 )#line:679
            print ('w_heel = {}'.format (O0O00O0OO000OOOO0 ))#line:680
            O00O0OO000O000OO0 =((O0O0000OOOOOO0OOO -OOO0O0OO00OOO00OO )**2 +(O0OO0OO00OO0O00OO -O0O0O0OOO0OOOO0OO )**2 )**0.5 #line:682
            print ('w_foot = {}'.format (O00O0OO000O000OO0 ))#line:683
            OOOOO00O0O000OOO0 =[OOO0O0OO00OOO00OO ,O0O0O0OOO0OOOO0OO ]#line:685
            O0OOOOO000OOO0OOO =[O0O0000OOOOOO0OOO ,O0OO0OO00OO0O00OO ]#line:686
            print ('w_point1 = [{}, {}]'.format (OOOOO00O0O000OOO0 [0 ],OOOOO00O0O000OOO0 [1 ]))#line:687
            print ('w_point2 = [{}, {}]'.format (O0OOOOO000OOO0OOO [0 ],O0OOOOO000OOO0OOO [1 ]))#line:688
            O00OO00OOO00O0OO0 =abs (OO0O0O0000OO0O0O0 -O0O0O0OOO0OOOO0OO )#line:690
            OO000O00O0O0000OO =abs (OO0O0O0000OO0O0O0 -O0OO0OO00OO0O00OO )#line:691
            print ('w_level_left = {}'.format (O00OO00OOO00O0OO0 ))#line:692
            print ('w_level_right = {}'.format (OO000O00O0O0000OO ))#line:693
            OO0OOOO0O00OOO00O =abs (O0O00O0O0O0O0OO0O [0 ]-OOO0O0OO00OOO00OO )#line:695
            O000OOOO00OOO00O0 =abs (O0O0000OOOOOO0OOO -O0O00O0O0O0O0OO0O [0 ])#line:696
            print ('w_len_left = {}'.format (OO0OOOO0O00OOO00O ))#line:697
            print ('w_len_right = {}'.format (O000OOOO00OOO00O0 ))#line:698
        print ('\n### 確認')#line:701
        OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,20000 )#line:703
        if test :#line:704
            ft .showc (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,'xy',OOO00OOO0O00OO0O0 ,O0O00O0O0O0O0OO0O ,OOOOO00O0O000OOO0 ,O0OOOOO000OOO0OOO )#line:705
        print ('\n### 足囲の取り出し')#line:718
        OOOOO0000O0O00000 =deepcopy (OOOOOOO00000O00OO )#line:721
        OO00OOOO0OOOO0O0O =deepcopy (O0O0OO000OOOOO0OO )#line:722
        OOOOO0OO000O00O00 =math .atan2 (O0OOOOO000OOO0OOO [0 ]-OOOOO00O0O000OOO0 [0 ],O0OOOOO000OOO0OOO [1 ]-OOOOO00O0O000OOO0 [1 ])#line:725
        OO0O000O0000O00O0 =math .degrees (OOOOO0OO000O00O00 )#line:726
        O0000OO0O0O0O0OO0 =90 -OO0O000O0000O00O0 #line:728
        if O0000OO0O0O0O0OO0 >180 :#line:730
            O0000OO0O0O0O0OO0 =-360 +O0000OO0O0O0O0OO0 #line:731
        if O0000OO0O0O0O0OO0 <-180 :#line:732
            O0000OO0O0O0O0OO0 =360 -O0000OO0O0O0O0OO0 #line:733
        OOOOO00O0O000OOO0 =ft .rotate_2D_z (OOOOO00O0O000OOO0 ,theta =O0000OO0O0O0O0OO0 )#line:737
        O0OOOOO000OOO0OOO =ft .rotate_2D_z (O0OOOOO000OOO0OOO ,theta =O0000OO0O0O0O0OO0 )#line:738
        OOOOO0000O0O00000 =ft .rotate_3D_z (OOOOO0000O0O00000 ,theta =O0000OO0O0O0O0OO0 )#line:739
        OOOO00OOO0O0OO0OO =(OOOOO0000O0O00000 [:,0 ]>OOOOO00O0O000OOO0 [1 ]-2 )*(OOOOO0000O0O00000 [:,0 ]<OOOOO00O0O000OOO0 [1 ]+2 )#line:742
        OOOOO0000O0O00000 =OOOOO0000O0O00000 [OOOO00OOO0O0OO0OO ]#line:743
        OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O [OOOO00OOO0O0OO0OO ]#line:744
        OOOOO00O0O000OOO0 [1 ]-=np .min (OOOOO0000O0O00000 [:,0 ])#line:747
        OOOOO00O0O000OOO0 [0 ]-=np .min (OOOOO0000O0O00000 [:,1 ])#line:748
        O0OOOOO000OOO0OOO [1 ]-=np .min (OOOOO0000O0O00000 [:,0 ])#line:749
        O0OOOOO000OOO0OOO [0 ]-=np .min (OOOOO0000O0O00000 [:,1 ])#line:750
        OOOOO0000O0O00000 [:,0 ]-=np .min (OOOOO0000O0O00000 [:,0 ])#line:751
        OOOOO0000O0O00000 [:,1 ]-=np .min (OOOOO0000O0O00000 [:,1 ])#line:752
        if test :#line:754
            ft .showc (OOOOO0000O0O00000 ,OO00OOOO0OOOO0O0O ,'xy',OOOOO00O0O000OOO0 ,O0OOOOO000OOO0OOO )#line:755
        print ('\n### 足囲')#line:759
        try :#line:761
            O0O0O0000O00O0000 #line:762
        except NameError :#line:763
            print ('\n### ダウンサンプル')#line:765
            OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOO0000O0O00000 ,OO00OOOO0OOOO0O0O ,200000 )#line:767
            print ('\n### 前処理')#line:770
            OOO00OOOO0OO000OO =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:773
            OO0O00O00O0O00O0O ,OO00O0O0OO0OO0O0O =OOO00OOOO0OO000OO .window_zoom_back (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,OOOOO00O0O000OOO0 [0 ],O0OOOOO000OOO0OOO [0 ])#line:775
            OO0O00O00O0O00O0O =OOO00OOOO0OO000OO .put_text (OO0O00O00O0O00O0O ,['1, Connect foot circumference','2, End before reach start point'])#line:779
            cv2 .rectangle (OO0O00O00O0O00O0O ,(0 ,window_size *2 //3 ),(window_size ,window_size ),(64 ,64 ,64 ),thickness =-1 )#line:781
            cv2 .putText (OO0O00O00O0O00O0O ,'Click to END & AUTO connect to start point',(0 ,window_size ),cv2 .FONT_HERSHEY_PLAIN ,1.5 ,(255 ,255 ,255 ),1 )#line:782
            O0OO0000OO0OOO00O ='step5'#line:788
            cv2 .namedWindow (O0OO0000OO0OOO00O )#line:789
            O00O0OO000OOOO00O =200 #line:790
            O00000OO0OO0OOO00 =pl_class (O00O0OO000OOOO00O )#line:791
            cv2 .setMouseCallback (O0OO0000OO0OOO00O ,OOO00OOOO0OO000OO .onMouse ,[O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O ,O00000OO0OO0OOO00 ])#line:792
            cv2 .imshow (O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O )#line:793
            cv2 .waitKey ()#line:794
            print ('\n### 後処理')#line:797
            OOO000OO000O000OO =OOO00OOOO0OO000OO .p /OO00O0O0OO0OO0O0O #line:800
            print (OOO000OO000O000OO )#line:801
            O0O0O0000O00O0000 =((OOO000OO000O000OO [0 ,0 ]-OOO000OO000O000OO [-1 ,0 ])**2 +(OOO000OO000O000OO [0 ,1 ]-OOO000OO000O000OO [-1 ,1 ])**2 )**0.5 #line:803
            for O00O0O0O00OO00O0O in range (1 ,len (OOO000OO000O000OO )):#line:806
                O0O0O0000O00O0000 +=((OOO000OO000O000OO [O00O0O0O00OO00O0O ,0 ]-OOO000OO000O000OO [O00O0O0O00OO00O0O -1 ,0 ])**2 +(OOO000OO000O000OO [O00O0O0O00OO00O0O ,1 ]-OOO000OO000O000OO [O00O0O0O00OO00O0O -1 ,1 ])**2 )**0.5 #line:807
            print ('c_foot = {}'.format (O0O0O0000O00O0000 ))#line:809
        O000O0OO0O0OOOO0O =O0O00O0O0O0O0OO0O [1 ]-OO0O00O0O0O0O000O #line:824
        O00O0OO00000O0O0O =O0O00O0O0O0O0OO0O [1 ]#line:825
        OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,20000 )#line:826
        if test :#line:827
            ft .showc (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,'xy',[0 ,O000O0OO0O0OOOO0O ],[0 ,O00O0OO00000O0O0O ])#line:828
        print ('\n### ガースポイント')#line:833
        try :#line:835
            OO0OO0O0OO000O000 #line:836
            OOO000OO0OO0O00OO #line:837
        except NameError :#line:838
            print ('\n### ダウンサンプル')#line:840
            print ('\n### 前処理')#line:845
            OOO00OOOO0OO000OO =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:848
            OO0O00O00O0O00O0O ,OO00O0O0OO0OO0O0O =OOO00OOOO0OO000OO .window_zoom_side (OO0O0O00O0000OOO0 ,O00000O00O0O0O0O0 )#line:851
            OOOOO00OOOO0OOOO0 =int ((O00O0OO00000O0O0O *rate2 +O000O0OO0O0OOOO0O *(1 -rate2 ))*OO00O0O0OO0OO0O0O )#line:855
            OO0OO000OO00000OO =int ((O00O0OO00000O0O0O *rate3 +O000O0OO0O0OOOO0O *(1 -rate3 ))*OO00O0O0OO0OO0O0O )#line:856
            cv2 .line (OO0O00O00O0O00O0O ,(OOOOO00OOOO0OOOO0 ,0 ),(OOOOO00OOOO0OOOO0 ,window_size ),(255 ,255 ,0 ))#line:857
            cv2 .line (OO0O00O00O0O00O0O ,(OO0OO000OO00000OO ,0 ),(OO0OO000OO00000OO ,window_size ),(255 ,254 ,0 ))#line:858
            OO0O00O00O0O00O0O =OOO00OOOO0OO000OO .put_text (OO0O00O00O0O00O0O ,['1, Heel girth front','2, Heel girth back'])#line:862
            O0OO0000OO0OOO00O ='step6'#line:868
            cv2 .namedWindow (O0OO0000OO0OOO00O )#line:869
            O00O0OO000OOOO00O =1 #line:870
            O00000OO0OO0OOO00 =pl_class (O00O0OO000OOOO00O )#line:871
            cv2 .setMouseCallback (O0OO0000OO0OOO00O ,OOO00OOOO0OO000OO .onMouse ,[O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O ,O00000OO0OO0OOO00 ])#line:872
            cv2 .imshow (O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O )#line:873
            cv2 .waitKey ()#line:874
            print ('\n### 後処理')#line:877
            OO0OO0O0OO000O000 =np .array ([OOOOO00OOOO0OOOO0 ,OOO00OOOO0OO000OO .p [0 ,1 ]])#line:880
            OOO000OO0OO0O00OO =np .array ([OO0OO000OO00000OO ,window_size //2 ])#line:881
            print (OO0OO0O0OO000O000 ,OOO000OO0OO0O00OO )#line:882
            OO0OO0O0OO000O000 [0 ]/=OO00O0O0OO0OO0O0O #line:885
            OO0OO0O0OO000O000 [1 ]=-(OO0OO0O0OO000O000 [1 ]-window_size //2 )/OO00O0O0OO0OO0O0O #line:886
            OOO000OO0OO0O00OO [0 ]/=OO00O0O0OO0OO0O0O #line:887
            OOO000OO0OO0O00OO [1 ]=-(OOO000OO0OO0O00OO [1 ]-window_size //2 )/OO00O0O0OO0OO0O0O #line:888
            print ('g_point1 = [{}, {}] #x,z'.format (OO0OO0O0OO000O000 [0 ],OO0OO0O0OO000O000 [1 ]))#line:889
            print ('g_point2 = [{}, {}] #x,z'.format (OOO000OO0OO0O00OO [0 ],OOO000OO0OO0O00OO [1 ]))#line:890
        OO0OO0O0O0OOO0O0O =OO0OO0O0OO000O000 [1 ]#line:893
        print ('g_step_height = {}'.format (OO0OO0O0O0OOO0O0O ))#line:894
        print ('\n### 確認')#line:897
        OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOOOO00000O00OO ,O0O0OO000OOOOO0OO ,20000 )#line:899
        if test :#line:900
            ft .showc (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,'xz',[OO0OO0O0OO000O000 [1 ],OO0OO0O0OO000O000 [0 ]],[OOO000OO0OO0O00OO [1 ],OOO000OO0OO0O00OO [0 ]])#line:901
        print ('\n### ガースの取り出し')#line:915
        OOOOO0000O0O00000 =deepcopy (OOOOOOO00000O00OO )#line:918
        OO00OOOO0OOOO0O0O =deepcopy (O0O0OO000OOOOO0OO )#line:919
        OOOOO0OO000O00O00 =math .atan2 (OOO000OO0OO0O00OO [1 ]-OO0OO0O0OO000O000 [1 ],OOO000OO0OO0O00OO [0 ]-OO0OO0O0OO000O000 [0 ])#line:922
        OO0O000O0000O00O0 =math .degrees (OOOOO0OO000O00O00 )#line:923
        O000O00O0OO000000 =90 +OO0O000O0000O00O0 #line:925
        if O000O00O0OO000000 >180 :#line:927
            O000O00O0OO000000 =-360 +O000O00O0OO000000 #line:928
        if O000O00O0OO000000 <-180 :#line:929
            O000O00O0OO000000 =360 -O000O00O0OO000000 #line:930
        OO0OO0O0OO000O000 =ft .rotate_2D_z (OO0OO0O0OO000O000 ,theta =O000O00O0OO000000 )#line:934
        OOO000OO0OO0O00OO =ft .rotate_2D_z (OOO000OO0OO0O00OO ,theta =O000O00O0OO000000 )#line:935
        OOOOO0000O0O00000 =ft .rotate_3D_y (OOOOO0000O0O00000 ,theta =O000O00O0OO000000 )#line:936
        OOO0O000OO00O00O0 =(OOOOO0000O0O00000 [:,0 ]>OO0OO0O0OO000O000 [0 ]-2 )*(OOOOO0000O0O00000 [:,0 ]<OOO000OO0OO0O00OO [0 ]+2 )#line:939
        OOOOO0000O0O00000 =OOOOO0000O0O00000 [OOO0O000OO00O00O0 ]#line:940
        OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O [OOO0O000OO00O00O0 ]#line:941
        OOOOO0000O0O00000 [:,2 ]-=OOO000OO0OO0O00OO [1 ]#line:944
        OO0OO0O0OO000O000 [1 ]-=OOO000OO0OO0O00OO [1 ]#line:945
        OOO000OO0OO0O00OO [1 ]-=OOO000OO0OO0O00OO [1 ]#line:946
        if test :#line:948
            ft .showc (OOOOO0000O0O00000 ,OO00OOOO0OOOO0O0O ,'xz',[OO0OO0O0OO000O000 [1 ],OO0OO0O0OO000O000 [0 ]],[OOO000OO0OO0O00OO [1 ],OOO000OO0OO0O00OO [0 ]])#line:949
            ft .showc (OOOOO0000O0O00000 ,OO00OOOO0OOOO0O0O ,'xy')#line:950
        print ('\n### ガース')#line:957
        try :#line:959
            OO00OO00OO0O0O000 #line:960
        except NameError :#line:961
            print ('\n### ダウンサンプル')#line:963
            OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO =ft .down_sample (OOOOO0000O0O00000 ,OO00OOOO0OOOO0O0O ,200000 )#line:965
            print ('\n### 前処理')#line:968
            OOO00OOOO0OO000OO =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:971
            OO0O00O00O0O00O0O ,OO00O0O0OO0OO0O0O =OOO00OOOO0OO000OO .window_zoom_back (OO0OO00OO0O00OO0O ,OOOOOOO00O00OOOOO ,0 ,0 )#line:973
            OO0O00O00O0O00O0O =OOO00OOOO0OO000OO .put_text (OO0O00O00O0O00O0O ,['1, Connect girth','2, End before reach start point'])#line:977
            cv2 .rectangle (OO0O00O00O0O00O0O ,(0 ,window_size *2 //3 ),(window_size ,window_size ),(64 ,64 ,64 ),thickness =-1 )#line:979
            cv2 .putText (OO0O00O00O0O00O0O ,'Click to END & AUTO connect to start point',(0 ,window_size ),cv2 .FONT_HERSHEY_PLAIN ,1.5 ,(255 ,255 ,255 ),1 )#line:980
            O0OO0000OO0OOO00O ='step7'#line:986
            cv2 .namedWindow (O0OO0000OO0OOO00O )#line:987
            O00O0OO000OOOO00O =200 #line:988
            O00000OO0OO0OOO00 =pl_class (O00O0OO000OOOO00O )#line:989
            cv2 .setMouseCallback (O0OO0000OO0OOO00O ,OOO00OOOO0OO000OO .onMouse ,[O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O ,O00000OO0OO0OOO00 ])#line:990
            cv2 .imshow (O0OO0000OO0OOO00O ,OO0O00O00O0O00O0O )#line:991
            cv2 .waitKey ()#line:992
            print ('\n### 後処理')#line:995
            OOO000OO000O000OO =OOO00OOOO0OO000OO .p /OO00O0O0OO0OO0O0O #line:998
            print (OOO000OO000O000OO )#line:999
            OO00OO00OO0O0O000 =((OOO000OO000O000OO [0 ,0 ]-OOO000OO000O000OO [-1 ,0 ])**2 +(OOO000OO000O000OO [0 ,1 ]-OOO000OO000O000OO [-1 ,1 ])**2 )**0.5 #line:1001
            for O00O0O0O00OO00O0O in range (1 ,len (OOO000OO000O000OO )):#line:1004
                OO00OO00OO0O0O000 +=((OOO000OO000O000OO [O00O0O0O00OO00O0O ,0 ]-OOO000OO000O000OO [O00O0O0O00OO00O0O -1 ,0 ])**2 +(OOO000OO000O000OO [O00O0O0O00OO00O0O ,1 ]-OOO000OO000O000OO [O00O0O0O00OO00O0O -1 ,1 ])**2 )**0.5 #line:1005
            print ('g_step = {}'.format (OO00OO00OO0O0O000 ))#line:1007
        O00OOOO0OO0O0OOOO =['l_foot','w_heel','w_foot','w_len_left','w_len_right','w_len_sum','w_level_left','w_level_right','c_foot','g_step_height','g_step']#line:1021
        OOOOOO000OOOO00O0 =[round (OO0O00O0O0O0O000O ,1 ),round (O0O00O0OO000OOOO0 ,1 ),round (O00O0OO000O000OO0 ,1 ),round (OO0OOOO0O00OOO00O ,1 ),round (O000OOOO00OOO00O0 ,1 ),round (OO0OOOO0O00OOO00O +O000OOOO00OOO00O0 ,1 ),round (O00OO00OOO00O0OO0 ,1 ),round (OO000O00O0O0000OO ,1 ),round (O0O0O0000O00O0000 ,1 ),round (OO0OO0O0O0OOO0O0O ,1 ),round (OO00OO00OO0O0O000 ,1 )]#line:1032
        return O00OOOO0OO0O0OOOO ,OOOOOO000OOOO00O0 #line:1034
if __name__ =='__main__':#line:1049
    file ='../test/サンプル太郎/sample.pckl'#line:1066
    paper_long =297 #line:1069
    paper_short =210 #line:1070
    window_size =1200 #line:1072
    dot_size =1 #line:1074
    cut_height =90 #line:1076
    rate1 =0.18 #line:1078
    rate2 =0.44 #line:1080
    rate3 =0.54 #line:1081
    test =1 #line:1083
    names ,values =vcfoot ().enkaku (file ,paper_long =paper_long ,paper_short =paper_short ,window_size =window_size ,dot_size =dot_size ,cut_height =cut_height ,rate1 =rate1 ,rate2 =rate2 ,rate3 =rate3 ,test =test )#line:1093
    print (names )#line:1096
    print (values )#line:1097
