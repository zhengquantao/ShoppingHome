from django.shortcuts import render
from django.http import JsonResponse
from Login.models import *
import uuid

save_id = []  # 创建一个空列表


def detail(request):
    id = request.GET.get('id')
    # user = request.GET.get('user')
    user = request.session.get('user')
    if id not in save_id:   # 去重
        save_id.append(id)
    if len(save_id) > 5:  # 默认最近5条浏览记录
        save_id.pop(0)
    request.session['recently'] = save_id

    if user:
        count = Car.objects.filter(user=user).count()
        if count:
            count = count
    else:
        user = ''
        count = ''
    item = ClassList.objects.filter(l_number=id)  # 更改浏览量
    item.update(see_nums=item[0].see_nums+1)
    detail_list = item.values('l_number', 'name', 'img_url', 'color', 'price', 'comment__content',
                              'comment__userinfo__nickname', 'see_nums', 'pay_nums')

    # 获取根评论
    all_comment = MComment.objects.filter(number__l_number=id).values('uname__name', 'dComment', 'date', 'cid').order_by('-date')
    # print('sssss', all_comment)
    # 子评论
    follow_comment = AComment.objects.filter(uname__number__l_number=id).values('uname__cid', 'cname__cname', 'cname__cComment', 'cname__date')

    # 猜你喜欢
    like = []
    guess_like = item.values('id')  # 得到这个id
    if guess_like[0]['id']-1 == 0:
        item = ClassList.objects.filter(id=2)
        like.append(item)
    else:
        item = ClassList.objects.filter(id=guess_like[0]['id']-1)
        like.append(item)
    return render(request, 'index/detail.html', {
        'detail_list': detail_list[0], 'username': user, "count": count, 'comment': all_comment, 'follow': follow_comment, 'like': like[0]})


# 根评论
def comment(request):
    # user = request.GET.get('user')
    comment = request.GET.get('comment')
    item_id = request.GET.get('cid')
    uid = uuid.uuid4()
    item = ClassList.objects.get(l_number=item_id)
    user = UserInfo.objects.get(name=request.session.get('user'))
    MComment.objects.create(dComment=comment, cid=uid, number=item, uname=user)

    return JsonResponse({'cid': uid})


# 子评论
def child_comment(request):
    uid = request.GET.get('uid')
    c_comment = request.GET.get('comment')
    CComment.objects.create(cname=request.session.get('user'), cComment=c_comment)
    cname = CComment.objects.get(cname=request.session.get('user'))
    uname = MComment.objects.get(cid=uid)
    AComment.objects.create(uname=uname, cname=cname)
    return JsonResponse({})
