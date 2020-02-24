#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,SelectField,FloatField
from wtforms.validators import DataRequired


class SymptomForm(FlaskForm): #功能一的表单
    sympt_name = StringField('病症:', validators=[DataRequired()])
    submit1 = SubmitField('提交')

class ScriptForm(FlaskForm): #功能二的表单
    sympt_name2 = StringField('病症：', validators=[DataRequired()])
    product_num = IntegerField('药品数量', render_kw={'size': "2"})
    people_age = SelectField('年龄段', choices=[(1, '成人'), (2, '儿童')], validators=[DataRequired('请选择年龄段')])
    specific_people = SelectField('特殊人群',
                                  choices=[(0, '否'), (1, '哺乳期妇女'), (2, '过敏患者'), (3, '妊娠期妇女'), (4, '老年人'), (5, '未成年人'),
                                           (6, '未成熟儿'), (7, '新生儿'), (8, '孕妇'), (9, '早产儿')])
    diseases = StringField('基础疾病')

    product1_name = StringField('药品1:')
    frequency1 = IntegerField('一日', render_kw={'size': "2"})
    fre1 = IntegerField('每几小时一次', render_kw={'size': "2"})
    amount11 = FloatField('一次', render_kw={'size': "2"})  # 一日几次的
    amount21 = FloatField('一次', render_kw={'size': "2"})  # 每几小时一次的
    usage1 = SelectField('用法',
                         choices=[(1, '口服'), (2, '注射'), (3, '静脉注射'), (4, '静脉滴注'), (5, '快速静脉注射'), (6, '吸入'), (7, '喷雾'),
                                  (8, '外用')])

    product2_name = StringField('药品2:')
    frequency2 = IntegerField('一日', render_kw={'size': "2"})
    fre2 = IntegerField('每几小时一次', render_kw={'size': "2"})
    amount12 = FloatField('一次', render_kw={'size': "2"})  # 一日几次的
    amount22 = FloatField('一次', render_kw={'size': "2"})  # 每几小时一次的
    usage2 = SelectField('用法',
                         choices=[(1, '口服'), (2, '注射'), (3, '静脉注射'), (4, '静脉滴注'), (5, '快速静脉注射'), (6, '吸入'), (7, '喷雾'),
                                  (8, '外用')])

    product3_name = StringField('药品3:')
    frequency3 = IntegerField('一日', render_kw={'size': "2"})
    fre3 = IntegerField('每几小时一次', render_kw={'size': "2"})
    amount13 = FloatField('一次', render_kw={'size': "2"})  # 一日几次的
    amount23 = FloatField('一次', render_kw={'size': "2"})  # 每几小时一次的
    usage3 = SelectField('用法',
                         choices=[(1, '口服'), (2, '注射'), (3, '静脉注射'), (4, '静脉滴注'), (5, '快速静脉注射'), (6, '吸入'), (7, '喷雾'),
                                  (8, '外用')])

    submit2 = SubmitField('提交处方')