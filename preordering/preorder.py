
from __future__ import print_function
import sys, os, json, shlex, re







customers = {}

order_count = {}




def add_customer(name):
  if name in customers:
    print('Error: customer {} already exists'.format(name), file=sys.stderr)
  else:
    customers[name] = {}
    print('Customer {} successfully added'.format(name), file=sys.stderr)


def remove_customer(name):
  if name not in customers:
    print('Error: customer {} does not exist'.format(name), file=sys.stderr)
  else:
    del customers[name]
    print('Customer {} successfully removed'.format(name), file=sys.stderr)


def list_customers():
  for name in sorted(customers):
    print(name)



def add_order(name,item, quantity=1):
  if quantity==0:
    print('Quantity is 0: no changes are made',file=sys.stderr)
  elif quantity<0:
    print('Error: cannot have negative quantity of {}'.format(quantity), file=sys.stderr)
  else:
    if name not in customers:
      print('Error: {} is not a customer'.format(name), file = sys.stderr)
    else:
      customers[name][item] = customers[name].get(item,0)+quantity
      order_count[item] = order_count.get(item,0)+quantity
      print('{} has successfully added {} order(s) of {} to their order'.format(
        name,quantity,item
        ), file = sys.stderr)


def list_orders(names):
  if not names:
    names = sorted(customers)
  for name in names:
    if name not in customers:
      print('Error: {} is not a customer'.format(name))
      continue
    print(name)
    for item,quantity in sorted(customers[name].iteritems()):
      print('\t{} x{}'.format(item,quantity))


def save_to_json(fname):
  proceed = True
  if os.path.exists(fname):
    print('Save Falied: {} already exists'.format(fname), file= sys.stderr)
    print('overwrite? (y/n): ',file=sys.stderr)
    proceed = raw_input().strip().lower()=='y'
  if proceed:
    with open(fname,'w') as f:
      json.dump(dict(customers=customers,order_count=order_count), f, sort_keys=True)


def load_json(fname):
  global customers,order_count
  if not os.path.exists(fname):
    print('Load falied: {} does not exist'.format(fname), file= sys.stderr)
  else:
    with open(fname,'r') as f:
      d = json.load(f)
      customers = d['customers']
      order_count = d['order_count']


def count_current_orders():
  for item,quantity in sorted(order_count.iteritems()):
    print('{} x{}'.format(item,quantity))


def clear_all():
  global customers, order_count
  order_count = {}
  customers = {}



def clear_customer(name):
  if name not in customers:
    print('Error: customer {} does not exist'.format(name), file=sys.stderr)
  else:
    for item,quantity in customers[name].iteritems():
      order_count[item] -= quantity
      if order_count[item]==0:
        del order_count[item]
    customers[name] = {}



def dump_report(stream):
  print('---------- ORDER SUMMARY -----------', file=stream)
  for name in sorted(customers):
    print(name+": ", file=stream)
    for item,quantity in sorted(customers[name].iteritems()):
      print('\t{} x{}'.format(item,quantity), file=stream)
    print(file=stream)
  print ('TOTAL ORDER COUNT: ',file=stream)
  for item,quantity in sorted(order_count.iteritems()):
    print('\t{} x{}'.format(item,quantity), file=stream)






def parse(cmd):
  call = cmd.pop(0)
  if call == 'addcustomer':
    if not cmd:
      print('Too few arguments:\nUsage: addcustomer <name>', file= sys.stderr)
    else:
      add_customer(cmd.pop(0))
  elif call == 'listcustomers':
    list_customers()
  elif call == 'removecustomer':
    if not cmd:
      print('Too few arguments:\nUsage: removecustomer <name>', file= sys.stderr)
    else:
      remove_customer(cmd.pop(0))
  elif call == 'addorder':
    if len(cmd)<2:
      print('Too few arguments:\nUsage: addorder <name> <item> [quantity=1]', file= sys.stderr)
    else:
      if len(cmd)>=3:
        cmd[2]= int(cmd[2])
      add_order(*cmd[:3])
  elif call == 'listorders':
    list_orders(cmd)
  elif call == 'save':
    if not cmd:
      print('JSON file not specified: using default.json', file=sys.stderr)
      fname = 'default.json'
    else:
      fname = cmd[0]
    save_to_json(fname)
  elif call == 'load':
    if not cmd:
      print('JSON file not specified: using default.json', file=sys.stderr)
      fname = 'default.json'
    else:
      fname = cmd[0]
    load_json(fname)
  elif call=='ordercounts':
    count_current_orders()
  elif call == 'clear':
    clear_all()
  elif call == 'clearcustomer':
    if not cmd:
      print('Too few arguments:\nUsage: clearcustomer <name>', file= sys.stderr)
    else:
      clear_customer(cmd.pop(0))
  elif call == 'report':
    stream = open(cmd[0],'w') if cmd else sys.stdout
    dump_report(stream)
    if cmd:
      stream.close()
  else:
    print('Unknown Call: {}'.format(call),file=sys.stderr)






def shell_loop():
  while 1:
    print("command> ", end='', file = sys.stderr)
    command = raw_input().strip()
    command = shlex.split(command)
    if command:
      if command[0] == 'exit':
        print('Thanks! Bye!', file= sys.stderr)
        sys.exit(0)
      parse(command)




def main():
  print('Welcome to the preorder tracker.', file = sys.stderr)

  shell_loop()









if __name__ == '__main__':
  main()





