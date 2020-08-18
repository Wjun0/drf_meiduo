import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_meiduo.settings.dev")
django.setup()
import time
from collections import OrderedDict

from django.conf import settings
from django.template import loader
# from goods.models import GoodsChannel

from contents.models import ContentCategory
from goods.models import GoodsChannel


def generate_static_index_html():
    '''生成静态主页html'''
    print('%s: genertae_static_index_html'%time.ctime())
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id','sequence')
    for channel in channels:
        group_id = channel.group_id
        if group_id not in categories:
            categories[group_id] = {'channels':[],'sub_cates':[]}
        cat1 = channel.category
        categories[group_id]['channels'].append({
            'id':cat1.id,
            'name':cat1.name,
            'url':channel.url
        })
        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
                categories[group_id]['sub_cates'].append(cat2)
    print(categories)

    #广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
    context = {
        'categories':categories,
        'contents':contents
    }
    template = loader.get_template('index.html')
    html_text = template.render(context=context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR,'index.html')
    with open(file_path,'w',encoding='utf-8') as f:
        f.write(html_text)


if __name__ == '__main__':

    generate_static_index_html()