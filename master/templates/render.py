from subprocess import check_output
from yaml import load, dump
from jinja2 import Template

################ get the variables value ##############
with open('variables.yml', 'r') as my_variables_file:
    # Update master ip address
    master_ip = check_output("awk 'END{print $1}' /etc/hosts", shell=True)
    my_variables_in_yaml=load(my_variables_file.read())
    my_variables_in_yaml.update({'host_ip':master_ip})

################ render proxy config file ###################
with open('proxy.j2') as temp, open('/etc/salt/proxy', 'w+') as f:
    my_template = Template(temp.read())
    f.write(my_template.render(my_variables_in_yaml))

################### render junos configuration file #################
with open('syslog.j2') as temp, open('/srv/salt/syslog.conf','w') as conf:
    my_template = Template(temp.read())
    conf.write(my_template.render(my_variables_in_yaml))

################### render pillar top file ################################
with open('pillars_top.j2') as temp, open('/srv/pillar/top.sls','w+') as f:
    my_template = Template(temp.read())
    f.write(my_template.render(my_variables_in_yaml))

################### render device pillar files ################################
with open('pillars_device.j2') as temp: 
    my_template = Template(temp.read())

    for item in my_variables_in_yaml['junos']:
        with open('/srv/pillar/' + item['name'] +'-details.sls','w+') as f:
            f.write(my_template.render(item))
