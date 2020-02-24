# coding=utf-8
from flask import Flask,render_template,request,redirect,url_for
from my_form import SymptomForm,ScriptForm
import config
from data import get_drug,get_drug_from_symptom,get_drug_from_product,get_caution_people_from_drug,get_prohibit_people_from_drug,\
    get_caution_symptom_from_drug,get_prohibit_symptom_from_drug,get_caution_drug_from_drug,get_prohibit_drug_from_drug,get_usage_from_product


app = Flask(__name__)
app.config.from_object(config)

@app.route('/',methods=['POST','GET']) #主页内容
def home():
    return render_template('home.html')


@app.route('/SearchDrug',methods=['POST','GET']) #功能一的实现
def SearchDrug():
    form=SymptomForm()
    if request.method=='POST':
        symptom=form.sympt_name.data
        return redirect(url_for('getdrug', symp_name=symptom)) #提交时重定向到getdrug
    return render_template('SearchDrug.html', symp_form=form)  #不提交时跳转到输入页面

@app.route('/SearchDrug/?<string:symp_name>') #功能一结果展示
def getdrug(symp_name):
    drug_result, product_result = get_drug(symp_name)
    return render_template('SuitableDrugs.html', drug_result=drug_result, product_result=product_result)

@app.route('/CheckScript', methods=['POST', 'GET'])
def checkScript():
    script_form = ScriptForm()
    if request.method == 'POST':
        symp2_name = script_form.sympt_name2.data
        true_product_num = script_form.product_num.data
        product_name = []
        product_use = []  # 口服/注射
        product_frequency = []
        product_amount1 = []
        product_fre = []
        product_amount2 = []
        product_name.append(script_form.product1_name.data)
        product_name.append(script_form.product2_name.data)
        product_name.append(script_form.product3_name.data)
        str = ['口服', '注射', '静脉注射', '静脉滴注', '快速静脉注射', '吸入', '喷雾', '外用']
        product_use.append(str[int(script_form.usage1.data) - 1])
        product_use.append(str[int(script_form.usage2.data) - 1])
        product_use.append(str[int(script_form.usage3.data) - 1])
        product_frequency.append(script_form.frequency1.data)
        product_frequency.append(script_form.frequency2.data)
        product_frequency.append(script_form.frequency3.data)
        product_amount1.append(script_form.amount11.data)
        product_amount1.append(script_form.amount12.data)
        product_amount1.append(script_form.amount13.data)
        product_fre.append(script_form.fre1.data)
        product_fre.append(script_form.fre2.data)
        product_fre.append(script_form.fre3.data)
        product_amount2.append(script_form.amount21.data)
        product_amount2.append(script_form.amount22.data)
        product_amount2.append(script_form.amount23.data)

        people_age=script_form.people_age.data
        str1=['否', '哺乳期妇女', '过敏患者','妊娠期妇女', '老年人', '未成年人','未成熟儿', '新生儿', '孕妇', '早产儿']
        specific_people=str1[int(script_form.specific_people.data)]
        disease=script_form.diseases.data

        product_num = 0
        for onename in product_name:
            if onename != '':
                product_num = product_num + 1
        if product_num != true_product_num:
            return '验证失败，填写的处方中药品数目与实际提交的药品数目不符'

        SuitableDrugs = get_drug_from_symptom(symp2_name)

        cnt = 0
        Drugs=[]
        for oneproductname in product_name:
            if not ((product_amount1 != '' and product_frequency != '') or (
                    product_amount2 != '' and product_fre != '')):
                return '验证失败，用量信息未填写完整'
            drugs=get_drug_from_product(oneproductname)
            Drugs.extend(drugs)
            for onedrug in drugs:  # 验证药品与疾病是否对应
                cautionPeo=get_caution_people_from_drug(onedrug)
                prohibitPeo=get_prohibit_people_from_drug(onedrug)
                cautionSym=get_caution_symptom_from_drug(onedrug)
                prohibitSym=get_prohibit_symptom_from_drug(onedrug)

                if specific_people!='否' and specific_people in prohibitPeo:  #验证人群是否需禁用
                    return '验证失败，该人群需禁用处方上的药品'
                if specific_people!='否' and specific_people in cautionPeo:  #验证人群是否需慎用
                    return '验证失败，该人群需慎用处方上的药品'
                if disease is not None and disease in prohibitSym:   #验证患有基础疾病是否该禁用
                    return '验证失败，患有该疾病的患者禁用处方上的药品'
                if disease is not None and disease in cautionSym:    #验证患有基础疾病是否该慎用
                    return '验证失败，患有该疾病的患者慎用处方上的药品'

                if onedrug in SuitableDrugs:
                    cnt = cnt + 1
        if cnt != product_num:
            return '验证失败，处方中的药品不应被用于治疗该疾病'

        for onedrug in Drugs:                        #验证处方中药品能否共用
            cautionDrugs = get_caution_drug_from_drug(onedrug)
            prohibitDrugs = get_prohibit_drug_from_drug(onedrug)
            for one_cautionDrug in cautionDrugs:
                if one_cautionDrug in Drugs:
                    return '验证失败，处方中药品共用需谨慎'
            for one_prohibitDrug in prohibitDrugs:
                if one_prohibitDrug in Drugs:
                    return '验证失败，处方中药品禁止共用'

        for oneproductname in product_name:  # 验证用法用量是否正确
            if (oneproductname != ''):
                Usage = get_usage_from_product(oneproductname)
                if Usage['usage'] == product_use[product_name.index(oneproductname)]:  # 用法

                    if Usage['frequency'] != None and Usage['frequency'][0] == '一':
                        index1 = Usage['frequency'].find('日')
                        index2 = Usage['frequency'].find('次')
                        result = Usage['frequency'][index1 + 1:index2]
                        index3 = -1
                        if Usage['frequency'].find('-') != -1:  # 解决有些是~，有些是-
                            index3 = Usage['frequency'].find('-')
                        elif Usage['frequency'].find('～') != -1:
                            index3 = Usage['frequency'].find('～')
                        if index3 == -1:  # 一个数字的情况  #频率
                            if int(result) != product_frequency[product_name.index(oneproductname)]:
                                return '验证失败，处方中药品的用药频率有误'
                            else:
                                print('pass frequency1')
                        elif not (int(result[0:index3]) <= product_frequency[product_name.index(oneproductname)] <= int(
                                result[index3 + 1:])):  # a-b的情况
                            return '验证失败，处方中药品的用药频率有误'
                        else:
                            print('pass frequency2')

                        if Usage['consumption'] != None and Usage['consumption'][0] != '':  # 用量
                            index = Usage['consumption'].find('/')
                            index_1 = -1
                            if Usage['consumption'].find('-') != -1: #这里的-需改为中文！！！！！！！！
                                index_1 = Usage['consumption'].find('-')
                            elif Usage['consumption'].find('～') != -1:
                                index_1 = Usage['consumption'].find('～')
                            if index == -1:  # 没有/kg/日
                                mg_index = Usage['consumption'].find('mg')
                                if mg_index != -1:  # 单位为mg
                                    result = Usage['consumption'][0:mg_index]
                                    if index_1 == -1 and float(result) != product_amount1[
                                        product_name.index(oneproductname)]:
                                        return '验证失败，处方中药品的用量有误'
                                    elif index_1 != -1 and not (float(result[0:index_1]) <= product_amount1[
                                        product_name.index((oneproductname))] <= float(result[index_1 + 1:])):
                                        return '验证失败，处方中药品的用量有误'
                                else:
                                    g_index = Usage['consumption'].find('g')  # 单位为g
                                    if g_index != -1:
                                        result = Usage['consumption'][0:g_index]
                                        if index_1 == -1 and float(result) * 1000 != product_amount1[
                                            product_name.index(oneproductname)]:
                                            return '验证失败，处方中药品的用量有误'
                                        elif index_1 != -1 and not (float(result[0:index_1]) * 1000 <= product_amount1[
                                            product_name.index((oneproductname))] <= float(result[index_1 + 1:])):
                                            return '验证失败，处方中药品的用量有误'

                    elif Usage['frequency'] != None and Usage['frequency'][0] == '每':
                        index1 = Usage['frequency'].find('每')
                        index2 = Usage['frequency'].find('小')
                        result = Usage['frequency'][index1 + 1:index2]
                        index3 = -1
                        if Usage['frequency'].find('-') != -1:  # 解决有些是~，有些是-
                            index3 = Usage['frequency'].find('-')
                        elif Usage['frequency'].find('～') != -1:
                            index3 = Usage['frequency'].find('～')
                        if index3 == -1:  # 一个数字的情况  #频率
                            if int(result) != product_fre[product_name.index(oneproductname)]:
                                return '验证失败，处方中药品的用药频率有误'
                            else:
                                print('pass fre1')
                        elif not (int(result[0:index3]) <= product_fre[product_name.index(oneproductname)] <= int(
                                result[index3 + 1:])):  # a-b的情况
                            return '验证失败，处方中药品的用药频率有误'
                        else:
                            print('pass fre2')

                        if Usage['consumption'] != None and Usage['consumption'][0] != '':  # 用量
                            index = Usage['consumption'].find('/')
                            index_1 = -1
                            if Usage['consumption'].find('-') != -1:  # 这里的-需改为中文！！！！！！！！
                                index_1 = Usage['consumption'].find('-')
                            elif Usage['consumption'].find('～') != -1:
                                index_1 = Usage['consumption'].find('～')

                            if index == -1:  # 没有/kg/日
                                mg_index = Usage['consumption'].find('mg')
                                if mg_index != -1:  # 单位为mg
                                    result = Usage['consumption'][0:mg_index]
                                    if index_1 == -1 and float(result) != product_amount2[
                                        product_name.index(oneproductname)]:
                                        return '验证失败，处方中药品的用量有误'
                                    elif index_1 != -1 and not (float(result[0:index_1]) <= product_amount2[
                                        product_name.index(oneproductname)] <= float(result[index_1 + 1:])):
                                        return '验证失败，处方中药品的用量有误'
                                else:
                                    g_index = Usage['consumption'].find('g')  # 单位为g
                                    if g_index != -1:
                                        result = Usage['consumption'][0:g_index]
                                        if index_1 == -1 and float(result) * 1000 != product_amount2[
                                            product_name.index(oneproductname)]:
                                            return '验证失败，处方中药品的用量有误'
                                        elif index_1 != -1 and not (float(result[0:index_1]) * 1000 <= product_amount2[
                                            product_name.index((oneproductname))] <= float(result[index_1 + 1:])):
                                            return '验证失败，处方中药品的用量有误'
                else:
                    return '验证失败，用法错误'
        return '验证成功'
    return render_template('CheckScript.html', scri_form=script_form)

if __name__ == '__main__': #直接运行本项目时执行
    app.run()