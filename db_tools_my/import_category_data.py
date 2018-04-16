import os
import sys
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#指定project根目录所在的目录
sys.path.insert(0,BASE_DIR)#将根目录添加到系统路径目录中,只能通过insert添加
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mxshop.settings")#指定环境变量，将会根据路径加环境变量找到settings
django.setup()#django初始化
#以上操作都是为了使models能单独拿出来用
from goods.models import GoodsCategory
# all_categorys = GoodsCategory.objects.all()
from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_intance = GoodsCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()