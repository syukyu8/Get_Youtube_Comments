import matplotlib.pyplot as plt
import datetime

i=0
count = 0
minus = 0
result = []
time = []
sec = []
new_left = []
#この秒数ごとのコメント数をみる
sep_sec = 30
#見たいデータを開く
with open('hogehoge.txt','r') as f:
    next(f)
    for line in f:
        try:
            #コメントが記入された時間だけ取り出す
            next(f)
            time.append(line)
            time[i] = time[i].rstrip('\n')
            time[i] = time[i].split(':')
            #マイナスになっている個数だけカウント
            if time[i][0][0] in '-':
                minus += 1
            #秒数に変換する
            if len(time[i]) <= 2:
                #分までしかない時
                sec.append(int(time[i][-1]) + int(time[i][-2])*60)
            else:
                #時間まである時
                sec.append(int(time[i][-1]) + int(time[i][-2])*60 + int(time[i][-3])*3600)
        except:
            pass
        i += 1
#マイナスになっている秒数をプラスにする
for i in range(minus):
    sec[i] *= -1
#sep_sec秒間ににコメントされた回数をカウント
check = sec[0]
for j in range(len(sec)):
    if sec[j] - check < sep_sec:
        count += 1
    else:
        check += sep_sec
        result.append(count)
        count = 1

print(result)

print(max(result))

left = []
for i in range(len(result)):
    left.append(i)

max_comment = [i for i, x in enumerate(result) if x == max(result)]
sort_comment = sorted(range(len(result)), key=lambda i:result[i])[-10:]

print(max_comment)
print(sort_comment)
#コメント数が多い順にソート
for i in sort_comment:
    td = datetime.timedelta(seconds=i * sep_sec)
    print(td)

left_ori = []
#ラベルを時間に変換
for i in range(len(left)):
    if  i == 0:
        pass
    elif i % 10 == 0:
        ff = datetime.timedelta(seconds=left[i]*sep_sec)
        ff = str(ff)
        new_left.append(ff)
        left_ori.append(left[i])
print(left_ori)
print(new_left)

#グラフ作成
fig, ax = plt.subplots()
rect = ax.bar(left,result,width=1.0)
ax.set_xticks(left_ori)
ax.set_xticklabels(new_left,fontsize=10,rotation=45)
ax.set_xlabel("comment_time")
ax.set_ylabel("comment_count")
plt.savefig('save.png')
plt.show()
