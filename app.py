import numpy as np



def remove_max(a):
  a=sorted(a,reverse = True)
  a[0]=0
  return a

def determine_ef_one(bundle_a,bundle_b,values_a,values_b):
  u_a_bundle_a = []
  u_b_bundle_b = []
  u_a_bundle_b = []
  u_b_bundle_a = []
  for j in bundle_a:
    u_a_bundle_a.append(values_a[j])
  for j in bundle_b:
    u_b_bundle_b.append(values_b[j])
  for j in bundle_a:
    u_b_bundle_a.append(values_a[j])
  if len(u_b_bundle_a) >=2:
      u_b_bundle_a=remove_max(u_b_bundle_a)
  for j in bundle_b:
    u_a_bundle_b.append(values_b[j])
  if len(u_a_bundle_b) >=2:
      u_a_bundle_b=remove_max(u_a_bundle_b)
  if sum(u_a_bundle_a) >= sum(u_a_bundle_b) and sum(u_b_bundle_b) >= sum(u_b_bundle_a):
    return 1
  else:
    return 0



def adjusted_winner(values_a,values_b):
  #a is winner, b is loser
  bundle_w_1 = []
  bundle_l_1 = []
  bundle_plus = []
  bundle_minus = []
  for j in range(len(values_a)):
    if values_a[j] >= 0 and values_b[j] <= 0:
      bundle_w_1.append(j)
    elif values_a[j] < 0 and values_b[j] >= 0:
      bundle_l_1.append(j)
    elif values_a[j] > 0 and values_b[j] > 0:
      bundle_plus.append(j)
    else:
      bundle_minus.append(j)
  bundle_a = bundle_w_1 + bundle_plus
  bundle_b = bundle_l_1 + bundle_minus
  adjusted_order=[]
  for j in range(len(bundle_plus+bundle_minus)):
    adjusted_order.append([j,values_a[j]/values_a[j]])
  adjusted_order = sorted(adjusted_order, reverse=True, key=lambda x: x[1])
  for list_adjusted in adjusted_order:
    print(bundle_a)
    print(bundle_b)
    print(determine_ef_one(bundle_a,bundle_b,values_a,values_b))
    if determine_ef_one(bundle_a,bundle_b,values_a,values_b) == 1:
      break
    if list_adjusted[0] in bundle_plus:
      bundle_a.remove(list_adjusted[0])
      bundle_b.append(list_adjusted[0])
    if list_adjusted[0] in bundle_minus:
      bundle_a.append(list_adjusted[0])
      bundle_b.remove(list_adjusted[0])
  return bundle_a, bundle_b




from flask import Flask, render_template, request, flash
# Formクラス及び使用するフィールドをインポート
from wtforms import (Form, BooleanField, IntegerField, PasswordField, StringField,
  SubmitField, TextAreaField)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
# 使用するvalidatorをインポート
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])   
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    alice_name = request.form['Alice']
    bob_name = request.form['Bob']
    num_of_task = request.form.get('num_of_task')
    v_a=[]
    print(request.form.getlist('sliderA_1'))
    for i in request.form.getlist('sliderA_1'):
      v_a.append(int(i))
    
    '''for i in [1,2,3]:
      vl_a='sliderA_'+str(i)
      v_a.append(float(request.form.get(vl_a)))'''
    v_b=[]
    print(request.form.getlist('sliderB_1'))
    for i in request.form.getlist('sliderB_1'):
      v_b.append(int(i))
    '''for i in [1,2,3]:
      vl_b='sliderB_'+str(i)
      v_b.append(float(request.form.get(vl_b)))'''
    print(v_a,v_b)
    if num_of_task:
      num_of_task = range(int(num_of_task))
    else:
        num_of_task=range(len(v_a))
    bundle_a, bundle_b = adjusted_winner(v_a,v_b)
    bundle_a_text=[]
    bundle_b_text=[]
    for i in bundle_a:
      bundle_a_text.append({'Task':"Task"+str(i+1), 'utility':v_a[i]})
    for i in bundle_b:
      bundle_b_text.append({'Task':"Task"+str(i+1), 'utility':v_a[i]})
    
    value_table=[]
    table_1=['']
    for i in range(len(v_a)):
      table_1.append('Task'+str(i+1))
    value_table.append(table_1)
    table_2=[alice_name]+v_a
    value_table.append(table_2)
    table_3=[bob_name]+v_b
    value_table.append(table_3)

    return render_template('register.html',a1=bundle_a_text,a2=bundle_b_text
    ,alice_name = alice_name,bob_name = bob_name, value_table=value_table,
    number_of_task=num_of_task)
  else:
    return render_template('register.html')
  




if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

    print(adjusted_winner([1,2,3],[2,2,2]))

