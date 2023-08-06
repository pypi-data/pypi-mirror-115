#!/usr/bin/env python3
"""
Copyright (c) 2011, Sony Pictures Imageworks
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import optparse,sys,os,time,json,glob,tempfile,datetime,getpass,re
try:from PypCustom import PypCustom
except ImportError:
	class PypCustom:0
try:from PypCustom import PowerPipeListCustom
except ImportError:
	class PowerPipeListCustom:0
try:from PypCustom import PypStrCustom
except ImportError:
	class PypStrCustom:0
try:from PypCustom import PypListCustom
except ImportError:
	class PypListCustom:0
try:from PypCustom import PypFunctionCustom
except ImportError:
	class PypFunctionCustom:0
class Colors:OFF=chr(27)+'[0m';RED=chr(27)+'[31m';GREEN=chr(27)+'[32m';YELLOW=chr(27)+'[33m';MAGENTA=chr(27)+'[35m';CYAN=chr(27)+'[36m';WHITE=chr(27)+'[37m';BLUE=chr(27)+'[34m';BOLD=chr(27)+'[1m';COLORS=[OFF,RED,GREEN,YELLOW,MAGENTA,CYAN,WHITE,BLUE,BOLD]
class NoColors:OFF='';RED='';GREEN='';YELLOW='';MAGENTA='';CYAN='';WHITE='';BLUE='';BOLD='';COLORS=[OFF,RED,GREEN,YELLOW,MAGENTA,CYAN,WHITE,BLUE,BOLD]
class PowerPipeList(list,PowerPipeListCustom):
	def __init__(self,*args):
		super(PowerPipeList,self).__init__(*args)
		try:PowerPipeListCustom.__init__(self)
		except AttributeError:pass
		self.pyp=Pyp()
	def divide(self,n_split):
		sub_out=[];out=[];n=0;pyp=Pyp();inputs=self.pyp.flatten_list(self)
		while inputs:
			input=inputs.pop(0);n=n+1;sub_out.append(input)
			if not n%n_split or not inputs:out.append([sub_out]);sub_out=[]
		return out
	def delimit(self,delimiter):return ' '.join(self.pyp.flatten_list(self)).split(delimiter)
	def oneline(self,delimiter=' '):flat_list=self.flatten_list(self);return delimiter.join(flat_list)
	def uniq(self):strings=self.pyp.flatten_list(self);return list(set(strings))
	def flatten_list(self,iterables):return self.pyp.flatten_list(iterables)
	def unlist(self):return self.pyp.flatten_list(self)
	def after(self,target,after_n=1):
		out=[];n=0;inputs=self.pyp.flatten_list(self)
		for input in inputs:
			n=n+1
			if target in input:out.append([[input]+inputs[n:n+after_n]])
		return out
	def before(self,target,before_n=1):
		out=[];n=0;inputs=self.pyp.flatten_list(self)
		for input in inputs:
			n=n+1
			if target in input:out.append([[input]+inputs[n-before_n-1:n-1]])
		return out
	def matrix(self,target,matrix_n=1):
		out=[];n=0;inputs=self.pyp.flatten_list(self)
		for input in inputs:
			n=n+1
			if target in input:out.append([inputs[n-matrix_n-1:n-1]+[input]+inputs[n:n+matrix_n]])
		return out
class PypStr(str,PypStrCustom):
	def __init__(self,*args):
		super(PypStr,self).__init__()
		try:PypStrCustom.__init__(self)
		except AttributeError:pass
		try:self.dir=os.path.split(self.rstrip('/'))[0];self.file=os.path.split(self)[1];self.ext=self.split('.')[-1]
		except:pass
	def trim(self,delim='/'):return PypStr(delim.join(self.split(delim)[0:-1]))
	def kill(self,*args):
		for arg in args:self=self.replace(arg,'')
		return PypStr(self)
	def letters(self):
		new_string=''
		for letter in list(self):
			if letter.isalpha():new_string=new_string+letter
			else:new_string=new_string+' '
		return[PypStr(x)for x in new_string.split()if x]
	def punctuation(self):
		new_string=''
		for letter in list(self):
			if letter in'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':new_string=new_string+letter
			else:new_string=new_string+' '
		return[PypStr(x)for x in new_string.split()if x]
	def digits(self):
		new_string=''
		for letter in list(self):
			if letter.isdigit():new_string=new_string+letter
			else:new_string=new_string+' '
		return[PypStr(x)for x in new_string.split()if x]
	def clean(self,delim='_'):
		for char in self:
			if not char.isalnum()and char not in['/','.',delim]:self=self.replace(char,' ')
		return PypStr(delim.join([x for x in self.split()if x.strip()]))
	def re(self,to_match):
		match=re.search(to_match,self)
		if match:return PypStr(match.group(0))
		else:return''
class PypList(list,PypListCustom):
	def __init__(self,*args):
		super(PypList,self).__init__(*args)
		try:PypListCustom.__init__(self)
		except AttributeError:pass
class Pyp:
	def __init__(self):
		self.history={}
		try:self.pwd=os.getcwd()
		except:self.pwd=''
	def get_custom_execute(self):
		custom_ob=PypCustom();custom_attrs=dir(custom_ob)
		if'custom_execute'in custom_attrs and custom_ob.custom_execute:final_execute=custom_ob.custom_execute
		else:final_execute=self.default_final_execute
		return final_execute
	def default_final_execute(self,cmds):
		for cmd in cmds:os.system(cmd)
	def get_custom_macro_paths(self):
		home=os.path.expanduser('~');custom_ob=PypCustom();custom_attrs=dir(custom_ob)
		if'user_macro_path'in custom_attrs:user_macro_path=custom_ob.user_macro_path
		else:user_macro_path=home+'/pyp_user_macros.json'
		if'group_macro_path'in custom_attrs:group_macro_path=custom_ob.group_macro_path
		else:group_macro_path=home+'/pyp_group_macros.json'
		return user_macro_path,group_macro_path
	def cmds_split(self,cmds,macros):
		cmd_array=[];cmd='';open_single=False;open_double=False;open_parenth=0;escape=False;letters=list(cmds)
		while letters:
			letter=letters.pop(0)
			if cmd and cmd[-1]=='\\':escape=True
			if letter=="'":
				if open_single and not escape:open_single=not open_single
				else:open_single=True
			if letter=='"':
				if open_double and not escape:open_double=not open_double
				else:open_double=True
			if not open_single and not open_double:
				if letter=='(':open_parenth=open_parenth+1
				if letter==')':open_parenth=open_parenth-1
			if cmd.strip()in macros and letter in['|','[','%',',','+',' ']:cmd=cmd.strip();letters=list('|'.join(macros[cmd]['command'])+letter+''.join(letters));cmd=''
			elif letter=='|'and not open_single and not open_double and not open_parenth:cmd_array.append(cmd);cmd=''
			else:cmd=cmd+letter
			escape=False
		if cmd.strip()in macros and not options.macro_save_name:return self.cmds_split('|'.join(cmd_array+macros[cmd]['command']),macros)
		else:cmd_array.append(cmd)
		return[x for x in cmd_array if x]
	def load_macros(self,macro_path):
		if os.path.exists(macro_path):macro_ob=open(macro_path);macros=json.load(macro_ob);macro_ob.close()
		else:macros={}
		return macros
	def write_macros(self,macros,macro_path,cmds):
		if options.macro_save_name:
			macro=options.macro_save_name;macro_name=macro.split('#')[0].strip();macros[macro_name]={};macros[macro_name]['command']=cmds;macros[macro_name]['user']=getpass.getuser();macros[macro_name]['date']=str(datetime.datetime.now()).split('.')[0]
			if'#'in macro:macros[macro_name]['comments']='#'+macro.split('#')[1].strip()
			else:macros[macro_name]['comments']=''
			macro_ob=open(macro_path,'w');json.dump(macros,macro_ob);macro_ob.close();self.load_macros(macro_path)
			if macro_name in macros:print(Colors.YELLOW+macro_name,'successfully saved!'+Colors.OFF);sys.exit()
			else:print(Colors.RED+macro_name,'was not saved...unknown error!'+Colors.OFF);sys.exit(1)
	def delete_macros(self,macros,macro_path):
		if options.macro_delete_name:
			if options.macro_delete_name in macros:del macros[options.macro_delete_name];json_ob=open(macro_path,'w');json.dump(macros,json_ob);json_ob.close();print(Colors.MAGENTA+options.macro_delete_name+' macro has been successfully obliterated'+Colors.OFF);sys.exit()
			else:print(Colors.RED+options.macro_delete_name+' does not exist'+Colors.OFF);sys.exit(1)
	def list_macros(self,macros):
		if options.macro_list or options.macro_find_name:
			macros_sorted=[x for x in macros];macros_sorted.sort()
			for macro_name in macros_sorted:
				if options.macro_list or options.macro_find_name in macro_name or options.macro_find_name in macros[macro_name]['user']:print(Colors.MAGENTA+macro_name+'\n\t '+Colors.YELLOW+macros[macro_name]['user']+'\t'+macros[macro_name]['date']+'\n\t\t'+Colors.OFF+'"'+'|'.join(macros[macro_name]['command'])+'"'+Colors.GREEN+'\n\t\t'+macros[macro_name].get('comments','')+Colors.OFF+'\n')
			sys.exit()
	def load_file(self):
		if options.text_file:
			if not os.path.exists(options.text_file):print(Colors.RED+options.text_file+' does not exist'+Colors.OFF);sys.exit()
			else:f=[x.rstrip()for x in open(options.text_file)];return f
		else:return[]
	def shell(self,command):sh=[x.strip()for x in os.popen(command).readlines()];return sh
	def shelld(self,command,*args):
		if not args:ofs=':'
		else:ofs=args[0]
		shd={}
		for line in [x.strip()for x in os.popen(command).readlines()]:
			try:key=line.split(ofs)[0];value=ofs.join(line.split(ofs)[1:]);shd[key]=value
			except IndexError:pass
		return shd
	def rekeep(self,to_match):
		match=[];flat_p=self.flatten_list(self.p)
		for item in flat_p:
			if re.search(to_match,item):match.append(item)
		if match:return True
		else:return False
	def relose(self,to_match):return not self.rekeep(to_match)
	def keep(self,*args):
		kept=[]
		for arg in args:
			flat_p=self.flatten_list(self.p)
			for item in flat_p:
				if arg in item:kept.append(arg)
		if kept:return True
		else:return False
	def lose(self,*args):return not self.keep(*args)
	def array_tracer(self,input,power_pipe=''):
		if not input:
			if options.keep_false or power_pipe:input=' '
			else:return''
		nf=0;output=''
		if power_pipe:n_index=Colors.MAGENTA+'[%s]'%self.n+Colors.GREEN;final_color=Colors.OFF
		else:n_index='';final_color=''
		if type(input)in[list,PypList,PowerPipeList]:
			for field in input:
				if not nf==len(input):
					if type(field)in[str,PypStr]:COLOR=Colors.GREEN
					else:COLOR=Colors.MAGENTA
					output=str(output)+Colors.BOLD+Colors.BLUE+'[%s]'%nf+Colors.OFF+COLOR+str(field)+Colors.GREEN
				nf=nf+1
			return n_index+Colors.GREEN+Colors.BOLD+'['+Colors.OFF+output+Colors.GREEN+Colors.BOLD+']'+Colors.OFF
		elif type(input)in[str,PypStr]:return n_index+str(input)+final_color
		elif type(input)in[int,float]:return n_index+Colors.YELLOW+str(input)+Colors.OFF
		elif type(input)is dict:
			for field in sorted(input,key=lambda x:x.lower()):output=output+Colors.OFF+Colors.BOLD+Colors.BLUE+field+Colors.GREEN+': '+Colors.OFF+Colors.GREEN+str(input[field])+Colors.BOLD+Colors.GREEN+',\n '
			return n_index+Colors.GREEN+Colors.BOLD+'{'+output.strip().strip(' ,')+Colors.GREEN+Colors.BOLD+'}'+Colors.OFF
		else:return n_index+Colors.MAGENTA+str(input)+Colors.OFF
	def cmd_split(self,cmds):
		string_format='%s';cmd_array=[];cmd='';open_quote=False;open_parenth=0;open_bracket=0
		for letter in cmds:
			if letter in["'",'"']:
				if cmd and cmd[-1]=='\\':open_quote=True
				else:open_quote=not open_quote
			if not open_quote:
				if letter=='(':open_parenth=open_parenth+1
				elif letter==')':open_parenth=open_parenth-1
				elif letter=='[':open_bracket=open_bracket+1
				elif letter==']':open_bracket=open_bracket-1
				if not open_parenth and not open_bracket and letter in[',','+']:cmd_array.append(cmd);cmd='';string_format=string_format+letter.replace('+','%s').replace(',',' %s');continue
			cmd=cmd+letter
		cmd_array.append(cmd);output=[(cmd_array,string_format)];return output
	def all_meta_split(self,input_str):
		for char in input_str:
			if not char.isalnum():input_str=input_str.replace(char,' ')
		return[x for x in input_str.split()if x.strip()]
	def string_splitter(self):whitespace=self.p.split(None);slash=self.p.split('/');underscore=self.p.split('_');colon=self.p.split(':');dot=self.p.split('.');minus=self.p.split('-');all=self.all_meta_split(self.p);comma=self.p.split(',');split_variables_raw={'whitespace':whitespace,'slash':slash,'underscore':underscore,'colon':colon,'dot':dot,'minus':minus,'all':all,'comma':comma,'w':whitespace,'s':slash,'u':underscore,'c':colon,'d':dot,'m':minus,'a':all,'mm':comma};split_variables=dict(((x,PypList([PypStr(y)for y in split_variables_raw[x]]))for x in split_variables_raw));return split_variables
	def join_and_format(self,join_type):
		temp_joins=[];derived_string_format=self.history[self.n]['string_format'][-1];len_derived_str_format=len(derived_string_format.strip('%').split('%'))
		if len(self.p)==len_derived_str_format:
			string_format=derived_string_format
			for sub_p in self.p:
				if type(sub_p)in[list,PypList]:temp_joins.append(join_type.join(sub_p))
				else:temp_joins.append(sub_p)
			return PypStr(string_format%tuple(temp_joins))
		else:return PypStr(join_type.join((PypStr(x)for x in self.p)))
	def array_joiner(self):whitespace=self.join_and_format(' ');slash=self.join_and_format(os.sep);underscore=self.join_and_format('_');colon=self.join_and_format(':');dot=self.join_and_format('.');minus=self.join_and_format('-');all=self.join_and_format(' ');comma=self.join_and_format(',');join_variables={'w':whitespace,'s':slash,'u':underscore,'c':colon,'d':dot,'m':minus,'a':all,'mm':comma,'whitespace':whitespace,'slash':slash,'underscore':underscore,'colon':colon,'dot':dot,'minus':minus,'all':all,'comma':comma};return join_variables
	def translate_preset_variables(self,translate_preset_variables,file_input,second_stream_input):
		presets={'n':self.kept_n,'on':self.n,'fpp':file_input,'spp':second_stream_input,'nk':1000+self.kept_n,'shell':self.shell,'shelld':self.shelld,'keep':self.keep,'lose':self.lose,'k':self.keep,'l':self.lose,'rekeep':self.rekeep,'relose':self.relose,'rek':self.rekeep,'rel':self.relose,'quote':'"','apost':"'",'qu':'"','dollar':'$','pwd':self.pwd,'date':datetime.datetime.now(),'env':os.environ.get,'glob':glob.glob,'letters':'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','digits':'0123456789','punctuation':'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~','str':PypStr};history=[]
		for hist in self.history[self.n]['history']:
			if type(hist)in(list,PypList):hist=self.unlist_p(hist)
			history.append(hist)
		presets['history']=presets['h']=history
		if options.text_file:
			try:fp=file_input[self.n]
			except IndexError:fp=''
			presets['fp']=fp
		try:sp=second_stream_input[self.n]
		except IndexError:sp=''
		presets['sp']=sp
		if self.history[self.n]['output']:presets['o']=self.history[self.n]['history'][0]
		else:presets['o']=''
		presets['original']=presets['o'];p=self.p
		if type(p)in[str]:presets['p']=PypStr(p)
		elif type(p)in[list]:presets['p']=PypList(p)
		else:presets['p']=p
		presets.update(PypFunctionCustom.__dict__);return presets
	def initialize_n(self):self.history[self.n]={};self.history[self.n]['error']='';self.history[self.n]['history']=[];self.history[self.n]['history'].append(self.p);self.history[self.n]['string_format']=[];self.history[self.n]['original_splits']={};self.history[self.n]['output']=True
	def safe_eval(self,cmd,variables):
		if not self.history[self.n]['error']and self.history[self.n]['output']:
			total_output=[]
			for cm_tuple in self.cmd_split(cmd):
				string_format=cm_tuple[1]
				for cm in cm_tuple[0]:
					try:output=eval(cm,variables)
					except KeyboardInterrupt:print(Colors.RED+'killed by user'+Colors.OFF);sys.exit()
					except Exception as err:self.history[self.n]['error']=Colors.RED+'error: '+str(err)+Colors.OFF,Colors.RED+cmd+Colors.OFF;break
					try:
						if output is True:output=self.p
					except:pass
					total_output.append(output)
				self.history[self.n]['string_format'].append(string_format)
			return total_output
	def get_user_input(self,total_output,second_stream_input,file_input,power_pipe):
		try:
			n=self.n
			if power_pipe=='pp'and total_output or not power_pipe:user_output=total_output
			elif power_pipe=='spp'and second_stream_input:user_output=[second_stream_input[n]]
			elif power_pipe=='fpp'and file_input:user_output=[file_input[n]]
			elif power_pipe:print(Colors.RED+"YOU'RE LIST VARIABLE DOES NOT EXIST: "+Colors.GREEN+power_pipe+Colors.OFF);sys.exit()
		except:user_output=[' ']
		return user_output
	def update_history(self,total_output,second_stream_input,file_input,power_pipe):
		if(not total_output or not[x for x in total_output if x]or self.history[self.n]['error'])and total_output!=[0]and not power_pipe:self.history[self.n]['history'].append(False);self.history[self.n]['output']=False
		else:
			string_format=self.history[self.n]['string_format'][-1];output_array=[];history_array=[];contains_list=False;user_input=self.get_user_input(total_output,second_stream_input,file_input,power_pipe);self.kept_n=self.kept_n+1
			for out in total_output:history_array.append(out);contains_list=True if type(out)not in[str,PypStr]else False
			for out in user_input:output_array.append(self.array_tracer(out,power_pipe))
			self.history[self.n]['output']=string_format%tuple(output_array)
			if contains_list:self.history[self.n]['history'].append(total_output)
			else:self.history[self.n]['history'].append(string_format%tuple(history_array))
	def flatten_list(self,iterables):
		out=[]
		try:
			if[x for x in iterables if type(x)in[str,PypStr]]:out=out+iterables
			else:
				for x in iterables:out=out+self.flatten_list(x)
		except:out=[iterables]
		return out
	def power_pipe_eval(self,cmd,inputs,second_stream_input,file_input,power_pipe_type):
		variables={};self.history={};padded_output=[];variables['str']=PypStr;variables['n']=self.kept_n;variables['on']=self.n;inputs=self.flatten_list(inputs);inputs=[x for x in inputs if self.unlist_p(x)is not False];variables['pp']=PowerPipeList(inputs);variables['spp']=PowerPipeList(second_stream_input);variables['fpp']=PowerPipeList(file_input)
		try:output=eval(cmd,variables)
		except KeyboardInterrupt:print(Colors.RED+'killed by user'+Colors.OFF);sys.exit()
		except Exception as err:print(Colors.RED+'error: '+str(err)+Colors.OFF,Colors.RED+cmd+Colors.OFF);sys.exit()
		if output is None:output=variables[power_pipe_type]
		if type(output)in[int,float]:output=[output]
		if type(output)in[str,PypStr,tuple]:output=[[output]]
		if[x for x in output if type(x)in[tuple]]:output=[PypList(x)for x in output if type(x)in[tuple]]
		if len(output)==1:power_pipe_type=''
		return output,power_pipe_type
	def detect_power_pipe(self,command,power_pipe_type):
		open_quote=False;cmd_raw=list(command);cmd=[]
		for letter in cmd_raw:
			if letter not in['"',"'"]and not letter.isalnum():letter=' '
			cmd.append(letter)
		cmds=''.join(cmd).split()
		for cmd in cmds:
			cmd=list(cmd);test_cmd=''
			while cmd:
				letter=cmd.pop(0);test_cmd=test_cmd+letter
				if not open_quote:
					if power_pipe_type==test_cmd and not cmd:return True
				if letter in["'",'"']:
					if cmd and cmd[0]=='\\':open_quote=True
					else:open_quote=not open_quote
		return False
	def format_input(self,cmd,input_set,second_stream_input,file_input):
		power_pipe=''
		if self.detect_power_pipe(cmd,'pp'):input_set,power_pipe=self.power_pipe_eval(cmd,input_set,second_stream_input,file_input,'pp');cmd='p'
		elif self.detect_power_pipe(cmd,'spp'):second_stream_input,power_pipe=self.power_pipe_eval(cmd,input_set,second_stream_input,file_input,'spp');cmd='p'
		elif self.detect_power_pipe(cmd,'fpp'):file_input,power_pipe=self.power_pipe_eval(cmd,input_set,second_stream_input,file_input,'fpp');cmd='p'
		return cmd,input_set,second_stream_input,file_input,power_pipe
	def unlist_p(self,p):
		if type(p)in[list,PypList]and len(p)==1:p=p[0]
		return p
	def process(self,inputs,file_input,cmds,second_stream_input):
		while cmds:
			self.n=-1;self.kept_n=0;cmd=cmds.pop(0);cmd,input_set,second_stream_input,file_input,power_pipe=self.format_input(cmd,inputs,second_stream_input,file_input);original_input_set=input_set[:]
			while input_set:
				self.p=self.unlist_p(input_set.pop(0));self.n=self.n+1;variables={}
				if not self.n in self.history:self.initialize_n()
				elif self.p is False:continue
				if type(self.p)in[str,PypStr]:
					variables=self.string_splitter()
					if not self.history[self.n]['original_splits']:self.history[self.n]['original_splits']=dict((('o'+x,variables[x])for x in variables))
					if not self.history[self.n]['output']:self.history[self.n]['original_splits']=dict((('o'+x,'')for x in variables))
				elif type(self.p)in[list,PypList]and not power_pipe:
					try:variables=self.array_joiner()
					except:pass
				variables.update(self.translate_preset_variables(original_input_set,file_input,second_stream_input));variables.update(self.history[self.n]['original_splits']);total_output=self.safe_eval(cmd,variables);self.update_history(total_output,second_stream_input,file_input,power_pipe)
			new_input=[self.history[x]['history'][-1]for x in self.history];self.process(new_input,file_input,cmds,second_stream_input)
	def output(self,total_cmds):
		execute_cmds=[]
		for self.history_index in self.history:
			error=self.history[self.history_index]['error']
			if not error or'list index out of range'in error[0]or'string index out of range'in error[0]:
				cmd=self.history[self.history_index]['output']
				if cmd:
					if options.execute:execute_cmds.append(cmd)
					else:print(cmd)
				elif options.keep_false:print()
			else:print(Colors.RED+self.history[self.history_index]['error'][0]+Colors.RED+' : '+self.history[self.history_index]['error'][1]+Colors.OFF)
		if execute_cmds:self.final_execute(execute_cmds)
	def initilize_input(self):
		if options.manual:print(Docs.manual);sys.exit()
		if options.unmodified_config:print(Docs.unmodified_config);sys.exit()
		rerun_path='/%s/pyp_rerun_%d.txt'%(tempfile.gettempdir(),os.getppid())
		if options.rerun:
			if not os.path.exists(rerun_path):
				gpid=int(os.popen('ps -p %d -oppid='%os.getppid()).read().strip());rerun_gpid_path='/%s/pyp_rerun_%d.txt'%(tempfile.gettempdir(),gpid)
				if os.path.exists(rerun_gpid_path):rerun_path=rerun_gpid_path
				else:print(Colors.RED+rerun_path+' does not exist'+Colors.OFF);sys.exit()
			pipe_input=[x.strip()for x in open(rerun_path)if x.strip()]
		elif options.blank_inputs:
			pipe_input=[];end_n=int(options.blank_inputs)
			for n in range(0,end_n):pipe_input.append('')
		elif options.no_input:pipe_input=['']
		else:
			pipe_input=[x.rstrip()for x in sys.stdin.readlines()if x.strip()]
			if not pipe_input:pipe_input=['']
		rerun_file=open(rerun_path,'w');rerun_file.write('\n'.join([str(x)for x in pipe_input]));rerun_file.close();inputs=pipe_input;return[[PypStr(x)]for x in inputs]
	def main(self):
		second_stream_input=[PypStr(x)for x in args[1:]];file_input=[PypStr(x)for x in self.load_file()];self.final_execute=self.get_custom_execute();user_macro_path,group_macro_path=self.get_custom_macro_paths();user_macros=self.load_macros(user_macro_path);group_macros=self.load_macros(group_macro_path);group_macros.update(user_macros);macros=group_macros;action_macros=group_macros if options.macro_group else user_macros;action_macros_path=group_macro_path if options.macro_group else user_macro_path;self.list_macros(macros);self.delete_macros(action_macros,action_macros_path)
		if not args:cmds=['p']
		else:cmds=self.cmds_split(args[0],macros)
		self.write_macros(action_macros,action_macros_path,cmds);inputs=self.initilize_input();self.process(inputs,file_input,cmds,second_stream_input);self.output(cmds)
class Docs:manual=' \n    ===================================================================================\n    PYED PIPER MANUAL\n    \n    pyp is a command line utility for parsing text output and generating complex\n    unix commands using standard python methods. pyp is powered by python, so any\n    standard python string or list operation is available.  \n    \n    The variable "p" represents EACH line of the input as a python string, so for\n    example, you can replace all "FOO" with "GOO" using "p.replace(\'FOO\',\'GOO\')".\n    Likewise, the variable "pp" represents the ENTIRE input as a python array, so\n    to sort the input alphabetically line-by-line, use "pp.sort()"\n    \n    Standard python relies on whitespace formating such as indentions. Since this \n    is not convenient with command line operations, pyp employs an internal piping\n    structure ("|") similar to unix pipes.  This allows passing of the output of\n    one command to the input of the next command without nested "(())" structures.\n    It also allows easy spliting and joining of text using single, commonsense \n    variables (see below).  An added bonus is that any subresult between pipes\n    is available, making it easy to refer to the original input if needed.\n    \n    Filtering output is straightforward using python Logic operations. Any output\n    that is "True" is kept while anything "False" is eliminated. So "p.isdigit()"\n    will keep all lines that are completely numbers. \n    \n    The output of pyp has been optimized for typical command line scenarios. For\n    example, if text is broken up into an array using the "split()" method, the\n    output will be conveniently numbered by field because a field selection is\n    anticipated.  If the variable  "pp" is employed, the output will be numbered\n    line-by-line to facilitate picking any particular line or range of lines. In\n    both cases, standard python methods (list[start:end]) can be used to select\n    fields or lines of interest. Also, the standard python string and list objects\n    have been overloaded with commonly used methods and attributes. For example,\n    "pp.uniq()" returns all unique members in an array, and p.kill(\'foo\') will\n    eliminate all  "foo" in the input.\n    \n    pyp commands can be easily saved to disk and recalled using user-defined macros,\n    so a complicated parsing operation requiring 20 or more steps can be recalled\n    easily, providing an alternative to quick and dirty scripts. For more advanced\n    users, these macros can be saved to a central location, allowing other users to\n    execute them.  Also, an additional text file (PypCustom.py) can be set up that\n    allows additional methods to be added to the pyp str and list methods, allowing\n    tight integration with larger facilities data structures or custom tool sets.\n    \n    -----------------------------------------------------------------------------------\n                                PIPING IN THE PIPER\n    -----------------------------------------------------------------------------------\n    You can pipe data WITHIN a pyp statement using standard unix style pipes ("|"),\n    where "p" now represents the evaluation of the python statement before the "|".\n    You can also refer back to the ORIGINAL, unadulterated input using the variable\n    "o" or "original" at any time...and the variable "h" or "history" allows you\n    to refer back to ANY subresult generated between pipes ("|"). \n    \n    All pyp statements should be enclosed in double quotes, with single quotes being\n    used to enclose any strings.'+Colors.YELLOW+'\n    \n         echo \'FOO IS AN \' | pyp "p.replace(\'FOO\',\'THIS\') | p + \'EXAMPLE\'"\n           ==> THIS IS AN EXAMPLE'+Colors.GREEN+"\n    \n    -----------------------------------------------------------------------------------\n                             THE TYPE OF COLOR IS THE TYPE\n    -----------------------------------------------------------------------------------\n    pyp uses a simple color and numerical indexing scheme to help you identify what \n    kind of objects you are working with. Don't worry about the specifics right now,\n    just keep in mind that different types can be readily identified:\n    \n    strings:                 hello world\n    \n    integers or floats:"+Colors.YELLOW+'      1984'+Colors.GREEN+'\n    \n    split-up line: '+Colors.BOLD+'          ['+Colors.BLUE+'[0]'+Colors.OFF+Colors.GREEN+'hello'+Colors.BOLD+Colors.BLUE+'[1]'+Colors.OFF+Colors.GREEN+'world'+Colors.BOLD+'] '+Colors.OFF+Colors.GREEN+'\n    \n    entire input list:       '+Colors.MAGENTA+'[0]'+Colors.GREEN+'first line\n'+Colors.OFF+Colors.MAGENTA+'                             [1]'+Colors.GREEN+'second line'+Colors.OFF+Colors.GREEN+'\n                \n    dictionaries:'+Colors.BOLD+'            {'+Colors.BLUE+'hello world'+Colors.BOLD+Colors.GREEN+': '+Colors.OFF+Colors.GREEN+'1984'+Colors.BOLD+'}'+Colors.OFF+Colors.GREEN+'\n    \n    other objects:'+Colors.MAGENTA+'           RANDOM_OBJECT'+Colors.GREEN+' \n    \n    The examples below will use a yellow/blue color scheme to seperate them\n    from the main text however. Also, all colors can be removed using the\n     --turn_off_color flag.\n    \n    -----------------------------------------------------------------------------------\n                                  STRING OPERATIONS\n    -----------------------------------------------------------------------------------\n    Here is a simple example for splitting the output of "ls" (unix file list) on \'.\':'+Colors.YELLOW+'\n    \n        ls random_frame.jpg | pyp "p.split(\'.\')"  \n            ==>  ['+Colors.BLUE+'[0]'+Colors.YELLOW+'random_frame'+Colors.BLUE+'[1]'+Colors.YELLOW+'jpg] '+Colors.GREEN+'             \n    \n    The variable "p" represents each line piped in from "ls".  Notice the output has\n    index numbers, so it\'s trivial to pick a particular field or range of fields,\n    i.e. pyp "p.split(\'.\')[0]"  is the FIRST field.  There are some pyp generated\n    variables that make this simpler, for example the variable "d" or "dot" is the\n    same as p.split(\'.\'):'+Colors.YELLOW+'\n        \n        ls random_frame.jpg | pyp "dot"  \n            ==> ['+Colors.BLUE+'[0]'+Colors.YELLOW+'random_frame'+Colors.BLUE+'[1]'+Colors.YELLOW+'jpg]\n        \n        ls random_frame.jpg | pyp "dot[0]"\n            ==>   random_frame'+Colors.GREEN+'\n    \n    To Join lists back together, just pipe them to the same or another built-in\n    variable(in this case "u", or "underscore"):'+Colors.YELLOW+'\n    \n        ls random_frame.jpg | pyp "dot"  \n            ==> ['+Colors.BLUE+'[0]'+Colors.YELLOW+'random_frame'+Colors.BLUE+'[1]'+Colors.YELLOW+'jpg]\n        \n        ls random_frame.jpg | pyp "dot|underscore"   \n            ==> random_frame_jpg '+Colors.GREEN+'\n    \n    To add text, just enclose it in quotes, and use "+" or "," just like python: '+Colors.YELLOW+'\n    \n        ls random_frame.jpg | pyp "\'mkdir seq.tp_\' , d[0]+ \'_v1/misc_vd8\'"  \n            ==> mkdir seq.tp_random_frame_v1/misc_vd8\'" '+Colors.GREEN+'\n            \n    A fundamental difference between pyp and standard python is that pyp allows you\n    to print out strings and lists on the same line using the standard "+" and ","\n    notation that is used for string construction. This allows you to have a string\n    and then print out the results of a particular split so it\'s easy to pick out\n    your field of interest: '+Colors.YELLOW+'\n    \n        ls random_frame.jpg | pyp "\'mkdir\', dot"  \n         ==> mkdir ['+Colors.BLUE+'[0]'+Colors.YELLOW+'random_frame'+Colors.BLUE+'[1]'+Colors.YELLOW+'jpg] '+Colors.GREEN+'\n    \n    In the same way, two lists can be displayed on the same line using "+" or ",".\n    If you are trying to actually combine two lists, enclose them in parentheses:'+Colors.YELLOW+'\n    \n        ls random_frame.jpg | pyp "(underscore + dot)" \n        ==> ['+Colors.BLUE+'[0]'+Colors.YELLOW+'random'+Colors.BLUE+'[1]'+Colors.YELLOW+'frame.jpg'+Colors.BLUE+'[2]'+Colors.YELLOW+'random_frame'+Colors.BLUE+'[3]'+Colors.YELLOW+'jpg] '+Colors.GREEN+'\n         \n    This behaviour with \'+\' and \',\' holds true in fact for ANY object, making\n    it easy to build statements without having to worry about whether they\n    are strings or not.\n        \n    -----------------------------------------------------------------------------------\n                               ENTIRE INPUT LIST OPERATIONS\n    -----------------------------------------------------------------------------------\n    To perform operations that operate on the ENTIRE array of std-in, Use the variable\n    "pp", which you can manipulate using any standard python list methods. For example,\n    to sort the input, use:'+Colors.YELLOW+'\n       \n       pp.sort()'+Colors.GREEN+'\n    \n    When in array context, each line will be numbered with it\'s index in the array,\n    so it\'s easy to, for example select the 6th line of input by using "pp[5]".\n    You can pipe this back to p to continue modifying this input on a \n    line-by-line basis: '+Colors.YELLOW+'\n    \n       pp.sort() | p  '+Colors.GREEN+'\n    \n    You can add arbitrary entries to your std-in stream at this point using \n    list addition. For example, to add an entry to the start and end:'+Colors.YELLOW+"\n    \n       ['first entry']  +  pp  +  ['last entry']  "+Colors.GREEN+" \n    \n    The new pp will reflect these changes for all future operations.\n    \n    There are several methods that have been added to python's normal list methods \n    to facilitate common operations. For example, keeping unique members or \n    consolidating all input to a single line can be accomplished with: "+Colors.YELLOW+'\n    \n       pp.uniq()\n       pp.oneline()'+Colors.GREEN+' \n    \n    Also, there are a few useful python math functions that work on lists of\n    integers or floats like sum, min, and max. For example, to add up \n    all of the integers in the last column of input: '+Colors.YELLOW+'\n    \n       whitespace[-1] | int(p) | sum(pp) '+Colors.GREEN+' \n    \n    \n    -----------------------------------------------------------------------------------\n                                  MATH OPERATIONS\n    -----------------------------------------------------------------------------------\n    To perform simple math, use the integer or float functions  (int() or float())\n    AND put the math in "()" + '+Colors.YELLOW+'\n    \n        echo 665 | pyp "(int(p) + 1)"\n           ==> 666 '+Colors.GREEN+'\n    -----------------------------------------------------------------------------------\n                                  LOGIC FILTERS\n    -----------------------------------------------------------------------------------\n    To filter output based on a python function that returns a Booleon (True or False),\n    just pipe the input to this function, and all lines that return True will keep\n    their current value, while all lines that return False will be eliminated. '+Colors.YELLOW+'\n    \n        echo 666 | pyp  "p.isdigit()"\n           ==> 666'+Colors.GREEN+'\n           \n    Keep in mind, that if the Boolean is True, the entire value of p is returned.\n    This comes in handy when you want to test on one field, but use something else.\n    For example, a[2].isdigit() will return p, not a[2] if a[2] is a digit.\n    \n    Standard python logic operators such as "and","or","not", and \'in\' work as well.\n    \n    For example to filter output based on the presence of "GOO" in the line, use this:'+Colors.YELLOW+'\n    \n        echo GOO | pyp "\'G\' in p"\n           ==> GOO'+Colors.GREEN+'\n    \n    The pyp functions "keep(STR)" and "lose(STR)", and their respective shortcuts,\n    "k(STR)" and "i(STR)", are very useful for simple OR style string\n    filtering. See below.\n    \n    Also note, all lines that test False (\'\', {}, [], False, 0) are eliminated from\n    the output completely. You can instead print out a blank line if something tests\n    false using --keep_false. This is useful if you need placeholders to keep lists \n    in sync, for example.\n    -----------------------------------------------------------------------------------\n                       SECOND STREAM, TEXT FILE, AND BLANK INPUT\n    -----------------------------------------------------------------------------------\n    Normally, pyp receives its input by piping into it like a standard unix shell\n    command, but sometimes it\'s necessary to combine two streams of inputs, such as\n    consolidating the output of two shell commands line by line.  pyp provides\n    for this with the second stream input. Essentially anything after the pyp\n    command that is not associated with an option flag is brought into pyp as\n    the second stream, and can be accessed seperately from the primary stream\n    by using the variable \'sp\'\n    \n    To input a second stream of data, just tack on strings or execute (use backticks)\n    a command to the end of the pyp command, and then access this array using the\n    variable \'sp\'  '+Colors.YELLOW+'\n    \n        echo random_frame.jpg | pyp "p, sp" `echo "random_string"`\n           ===> random_frame.jpg random_string'+Colors.GREEN+"\n           \n    In a similar way, text input can be read in from a text file using the \n    --text_file flag. You can access the entire file as a list using the variable\n    'fpp', while the variable 'fp' reads in one line at a time. This text file\n    capability is very useful for lining up std-in data piped into pyp with\n    data in a text file like this:"+Colors.YELLOW+' \n    \n        echo normal_input | pyp -text_file example.txt "p, fp" '+Colors.GREEN+"\n    \n    This setup is geared mostly towards combining data from std-in with that in\n    a text file.  If the text file is your only data, you should cat it, and pipe\n    this into pyp.\n    \n    If you need to generate output from pyp with no input, use --blank_inputs.\n    This is useful for generating text based on line numbers using the 'n'\n    variable.\n    \n    -----------------------------------------------------------------------------------\n                       TEXT FILE AND SECOND STREAM LIST OPERATIONS\n    -----------------------------------------------------------------------------------\n    List operations can be performed on file inputs and second stream \n    inputs using the variables spp and fpp, respectively.  For example to sort\n    a file input, use: "+Colors.YELLOW+'\n    \n       fpp.sort() '+Colors.GREEN+'\n       \n    Once this operation takes place, the sorted fpp will be used for all future\n    operations, such as referring to the file input line-by-line using fp.  \n    \n    You can add these inputs to the std-in stream using simple list\n    additions like this: '+Colors.YELLOW+' \n    \n        pp + fpp '+Colors.GREEN+'\n    \n    If pp is 10 lines, and fpp is 10 line, this will result in a new pp stream \n    of 20 lines. fpp will remain untouched, only pp will change with this \n    operation.   \n    \n    Of course, you can trim these to your needs using standard\n    python list selection techniques: '+Colors.YELLOW+'\n    \n        pp[0:5] + fpp[0:5] '+Colors.GREEN+'\n    \n    This will result in a new composite input stream of 10 lines. \n    \n    Keep in mind that the length of fpp and spp is trimmed to reflect\n    that of std-in.  If you need to see more of your file or second\n    stream input, you can extend your std-in stream simply:'+Colors.YELLOW+"\n    \n        pp + ['']*10 "+Colors.GREEN+'\n          \n    will add 10 blank lines to std-in, and thus reveal another 10\n    lines of fpp if available.\n    \n    \n    -----------------------------------------------------------------------------------\n                                  MACRO USAGE\n    -----------------------------------------------------------------------------------\n    Macros are a way to permently store useful commands for future recall. They are\n    stored in your home directory by default. Facilites are provided to store public\n    macros as well, which is useful for sharing complex commands within your work group.\n    Paths to these text files can be reset to anything you choose my modifying the\n    PypCustom.py config file.  Macros can become quite complex, and provide\n    a useful intermediate between shell commands and scripts, especially for solving\n    one-off problems.  Macro listing, saving, deleting, and searching capabilities are\n    accessible using --macrolist, --macro_save, --macro_delete, --macro_find flags.\n    Run pyp --help for more details.\n    \n    you can pyp to and from macros just like any normal pyp command. '+Colors.YELLOW+'\n        pyp "a[0]| my_favorite_macros | \'ls\', p" '+Colors.GREEN+'\n    \n    Note, if the macro returns a list, you can access individual elements using\n    [n] syntax:'+Colors.YELLOW+'\n        pyp "my_list_macro[2]" '+Colors.GREEN+'\n    \n    Also, if the macro uses %s, you can append a %(string,..) to then end to string\n    substitute: '+Colors.YELLOW+'\n        pyp "my_string_substitution_macro%(\'test\',\'case\')" '+Colors.GREEN+'\n    \n    By default, macros are saved in your home directory. This can be modifed to any \n    directory by modifying the user_macro_path attribute in your PypCustom.py. If\n    you work in a group, you can also save macros for use by others in a specific\n    location by modifying group_macro_path. See the section below on custom \n    methods about how to set up this file.\n    -----------------------------------------------------------------------------------\n                                  CUSTOM METHODS\n    -----------------------------------------------------------------------------------\n    pyed pyper relies on overloading the standard python string and list objects\n    with its own custom methods.  If you\'d like to try writing your own methods\n    either to simplify a common task or integrate custom functions using a \n    proprietary API, it\'s straightforward to do. You\'ll have to setup a config\n    file first:\n        \n        pyp --unmodified_config > PypCustom.py\n        sudo chmod 666 PypCustom.py\n    \n    There are example functions for string, list, powerpipe, and generic methods.\n    to get you started. When pyp runs, it looks for this text file and automatically\n    loads any found functions, overloading them into the appropriate objects. You\n    can then use your custom methods just like any other pyp function.\n    -----------------------------------------------------------------------------------\n                                  TIPS AND TRICKS\n    -----------------------------------------------------------------------------------\n    If you have to cut and paste data (from an email for example), execute pyp, paste\n    in your data, then hit CTRL-D.  This will put the data into the disk buffer. Then,\n    just rerun pyp with --rerun, and you\'ll be able to access this data for further\n    pyp manipulations!\n    \n    If you have split up a line into a list, and want to process this list line by \n    line, simply pipe the list to pp and then back to p: pyp "w | pp |p"\n    \n    Using --rerun is also great way to buffer data into pyp from long-running scripts\n    \n    pyp is an easy way to generate commands before executing them...iteratively keep\n    adding commands until you are confident, then use the --execute flag or pipe them\n    to sh.  You can use ";" to set up dependencies between these commands...which is\n    an easy way to work out command sequences that would typically be executed in a \n    "foreach" loop.\n    \n    Break out complex intermediate steps into macros. Macros can be run at any point in a \n    pyp command.\n    \n    If you find yourself shelling out constantly to particular commands, it might \n    be worth adding python methods to the PypCustom.py config, especially if you\n    are at a large facility.\n    \n    Many command line tools (like stat) use a KEY:VALUE format. The shelld function\n    will turn this into a python dictionary, so you can access specific data using\n    their respective keys by using something like this: shelld(COMMAND)[KEY] \n    \n    ===================================================================================\n    HERE ARE THE BUILT IN VARIABLES:\n        \n        STD-IN (PRIMARY INPUT)\n        -------------\n        p        line-by-line std-in variable. p represents whatever was \n                 evaluated to before the previous pipe (|).\n        \n        pp       python list of ALL std-in input. In-place methods like\n                 sort() will work as well as list methods like sorted(LIST)\n        \n        SECOND STREAM\n        --------------\n        sp       line-by-line input second stream input, like p, but from all \n                 non-flag arguments AFTER pyp command: pyp "p, sp" SP1 SP2 SP3 ...\n        \n        spp      python list of ALL second stream list input. Modifications of\n                 this list will be picked up with future references to sp \n        \n        FILE INPUT\n        --------------\n        fp       line-by-line file input using --text_file TEXT_FILE. fp on \n                 the first line of output is the first line of the text file\n        \n        fpp      python list of ALL text file input. Modifications of\n                 this list will be picked up with future references to fp \n        \n        \n        COMMON VARIABLES\n        ----------------\n        original original line by line input to pyp    \n        o        same as original    \n        \n        quote    a literal "      (double quotes can\'t be used in a pyp expression)\n        paran    a literal \'\n        dollar   a literal $\n    \n        n        line counter (1st line is 0, 2nd line is 1,...use the form "(n+3)"\n                 to modify this value. n changes to reflect filtering and list ops.\n        nk       n + 1000\n        \n        date     date and time. Returns the current datetime.datetime.now() object.\n        pwd      present working directory\n        \n        history  history array of all previous results:\n                   so pyp "a|u|s|i|h[-3]" shows eval of s\n        h        same as history\n        \n        digits   all numbers [0-9]\n        letters  all upper and lowercase letters (useful when combined with variable n).\n                 letters[n] will print out "a" on the first line, "b" on the second...\n        punctuation all punctuation [!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]\n        \n        \n    ===================================================================================\n    THE FOLLOWING ARE SPLIT OR JOINED BASED ON p BEING A STRING OR AN ARRAY:\n        \n        s  OR slash          p split/joined on "/"        \n        d  OR dot            p split/joined on "."        \n        w  OR whitespace     p split/joined on whitespace (on spaces,tabs,etc)\n        u  OR underscore     p split/joined on \'_\'       \n        c  OR colon          p split/joined on \':\'       \n        mm OR comma          p split/joined on \',\'        \n        m  OR minus          p split/joined on \'-\'        \n        a  OR all            p split on [\' \'-_=$...] (on "All" metacharacters)\n    \n    Also, the ORIGINAL INPUT (history[0]) lines are split on delimiters as above, but \n    stored in os, od, ow, ou, oc, omm, om and oa as well as oslash, odot, owhitepace,\n    ocomma, ominus, and oall'+Colors.GREEN+'\n    \n    ===================================================================================\n    HERE ARE THE BUILT IN FUNCTIONS AND ATTRIBUTES: \n    \n       Function                Notes\n       --------------------------------------------------------------------------------\n            STRING     (all python STRING methods like p.replace(STRING1,STRING2) work)\n       --------------------------------------------------------------------------------\n        p.digits()           returns a list of contiguous numbers present in p\n        p.letters()          returns a list of contiguous letters present in p\n        p.punctuation()      returns a list of contiguous punctuation present in p\n        \n        p.trim(delimiter)    removes last field from string based on delimiter\n                             with the default being "/"\n        p.kill(STR1,STR2...) removes specified strings \n        p.clean(delimeter)   removes all metacharacters except for slashes, dots and \n                             the joining delimeter (default is "_")\n        p.re(REGEX)          returns portion of string that matches REGEX regular \n                             expression. works great with p.replace(p.re(REGEX),STR) \n        \n        p.dir                directory of path\n        p.file               file name of path\n        p.ext                file extension (jpg, tif, hip, etc) of path\n       \n        These fuctions will work with all pyp strings eg: p, o, dot[0], p.trim(), etc. \n        Strings returned by native python functions (like split()) won\'t have these \n        available, but you can still access them using str(STRING). Basically,\n        manually recasting anything using as a str(STRING) will endow them with \n        the custom pyp methods and attributes.\n       \n       --------------------------------------------------------------------------------                                                    \n            LIST        (all LIST methods like pp.sort(), pp[-1], and pp.reverse() work)\n       --------------------------------------------------------------------------------\n       pp.delimit(DELIM)     split input on delimiter instead of newlines\n       pp.divide(N)          consolidates N consecutive lines to 1 line. \n       pp.before(STRING, N)  searches for STRING, colsolidates N lines BEFORE it to\n                             the same line. Default N is 1. \n       pp.after(STRING, N)   searches for STRING, colsolidates N lines AFTER  it to\n                             same line. Default N is 1.\n       pp.matrix(STRING, N)  returns pp.before(STRING, N) and pp.after(STRING, N).\n                             Default N is 1.\n       pp.oneline(DELIM)     combines all list elements to one line with delimiter.\n                             Default delimeter is space.\n       pp.uniq()             returns only unique elements\n       pp.unlist()           breaks up ALL lists up into seperate single lines\n       \n       pp + [STRING]         normal python list addition extends list\n       pp + spp + fpp        normal python list addition combines several inputs.\n                             new input will be pp; spp and fpp are unaffected.\n       sum(pp), max(pp),...  normal python list math works if pp is properly cast\n                             i.e. all members of pp should be integers or floats.\n       \n       These functions will also work on file and second stream lists:  fpp and spp\n       \n       \n       --------------------------------------------------------------------------------                                                    \n            NATIVE PYP FUNCTIONS\n       --------------------------------------------------------------------------------\n       keep(STR1,STR2,...)   keep all lines that have at least one STRING in them\n       k(STR1,STR2,...)      shortcut for keep(STR1,STR2,...)\n       lose(STR1,STR2,...)   lose all lines that have at least one STRING in them\n       l(STR1,STR2,...)      shortcut for lose(STR1,STR2,...)\n       \n       rekeep(REGEX)         keep all lines that match REGEX regular expression\n       rek(REGEX)            shortcut for rekeep(REGEX)\n       relose(REGEX)         lose all lines that match REGEX regular expression\n       rel(REGEX)            shortcut for relose(REGEX)\n       \n       shell(SCRIPT)         returns output of SCRIPT in a list.\n       shelld(SCRIPT,DELIM)  returns output of SCRIPT in dictionary key/value seperated \n                             on \':\' (default) or supplied delimeter\n       env(ENVIROMENT_VAR)   returns value of evironment variable using os.environ.get()\n       glob(PATH)            returns globed files/directories at PATH. Make sure to use\n                             \'*\' wildcard\n       str(STR)              turns any object into an PypStr object, allowing use \n                             of custom pyp methods as well as normal string methods. \n    \n    SIMPLE EXAMPLES:\n    ===================================================================================\n       pyp "\'foo \' + p"                 ==>  "foo" + current line\n       pyp "p.replace(\'x\',\'y\') | p + o" ==>  current line w/replacement + original line \n       pyp "p.split(\':\')[0]"            ==>  first field of string split on \':\'\n       pyp "slash[1:3]"                 ==>  array of fields 1 and 2 of string split on \'/\'\n       pyp "s[1:3]|s"                   ==>  string of above joined with \'/\'\n    '+Colors.OFF;unmodified_config='\n#!/usr/bin/env python\n# This must be saved in same directory as pyp (or be in the python path)\n# make sure to name this PypCustom.py and change permission to 666\n\nimport sys\nimport os\n\n\nclass Colors(object):\n    OFF = chr(27) + \'[0m\'\n    RED = chr(27) + \'[31m\'\n    GREEN = chr(27) + \'[32m\'\n    YELLOW = chr(27) + \'[33m\'\n    MAGENTA = chr(27) + \'[35m\'\n    CYAN = chr(27) + \'[36m\'\n    WHITE = chr(27) + \'[37m\'\n    BLUE = chr(27) + \'[34m\'\n    BOLD = chr(27) + \'[1m\'\n    COLORS = [OFF, RED, GREEN, YELLOW, MAGENTA, CYAN, WHITE, BLUE, BOLD]\n\n\nclass NoColors(object):\n    OFF = \'\'\n    RED = \'\'\n    GREEN =\'\'\n    YELLOW = \'\'\n    MAGENTA = \'\'\n    CYAN = \'\'\n    WHITE =\'\'\n    BLUE =  \'\'\n    BOLD =  \'\'\n    COLORS = [OFF, RED, GREEN, YELLOW, MAGENTA, CYAN, WHITE, BLUE, BOLD]\n\n\nclass PypCustom(object):\n    \'modify below paths to set macro paths\'\n    def __init__(self):\n        self.user_macro_path = os.path.expanduser(\'~\')+ \'/pyp_user_macros.json\'\n        self.group_macro_path = os.path.expanduser(\'~\')+ \'/pyp_user_macros.json\'\n        self.custom_execute = False\n\n\nclass PowerPipeListCustom():\n    \'this is used for pp functions (list fuctions like sort) that operate on all inputs at once.\'\n    def __init__(self, *args):\n        pass\n    \n    def test(self):\n        print \'test\' #pp.test() will print "test"\n\n\nclass PypStrCustom():   \n    \'this is used for string functions using p and other pyp string variables\'\n    def __init__(self, *args):\n        self.test_attr = \'test attr\'\n    \n    def test(self):\n        print \'test\' #p.test() will print "test" is p is a str\n    \n    \nclass PypListCustom():\n    def __init__(self, *args):\n        pass\n\n    def test(self):\n        print \'test\' #p.test() will print "test" is p is a list broken up from a str\n\n\nclass PypFunctionCustom(object):\n    \'this is used for custom functions and variables (non-instance)\'\n    test_var = \'works\'\n    \n    def __init__(self, *args):\n        pass\n    \n    def test(self):\n        print \'working func \'  + self\n';usage='    \npyp is a python-centric command line text manipulation tool.  It allows you to format, replace, augment\nand otherwise mangle text using standard python syntax with a few golden-oldie tricks from unix commands\nof the past. You can pipe data into pyp or cut and paste text, and then hit ctrl-D to get your input into pyp.  \n    \nAfter it\'s in, you can use the standard repertoire of python commands to modify the text. The key variables\nare "p", which represents EACH LINE of the input as a PYTHON STRING.  and "pp", which represents ALL of the\ninputs as a PYTHON ARRAY. \n\nYou can pipe data WITHIN a pyp statement using standard unix style pipes ("|"), where "p" now represents the\nevaluation of the python statement before the "|". You can also refer back to the ORIGINAL, unadulterated\ninput using the variable "o" or "original" at any time...and the variable "h" or "history" allows you\nto refer back to ANY subresult generated between pipes ("|"). \n\nAll pyp statements should be enclosed in double quotes, with single quotes being used to enclose any strings.\n\n     echo \'FOO IS AN \' | pyp "p.replace(\'FOO\',\'THIS\') | p + \'EXAMPLE\'"\n       ==> THIS IS AN EXAMPLE\n    \nSplitting texton metacharacters is often critical for picking out particular fields of interest,\nso common SPLITS and JOINS have been assigned variables. For example, "underscore" or "u" will split a string\nto an array based on undercores ("_"), while "underscore" or "u" will ALSO join an array with underscores ("_") \nback to a string.  \n\nHere are a few key split/join variables; run with --manual for all variable and see examples below in the string section.\n    \n    s OR slash           splits AND joins on "/"\n    u OR underscore      splits AND joins on "_"\n    w OR whitespace      splits on whitespace (spaces,tabs,etc) AND joins with spaces\n    a OR all             splits on ALL metacharacters [!@#$%^&*()...] AND joins with spaces\n    \nEXAMPLES:\n------------------------------------------------------------------------------\n              List Operations              # all python list methods work\n------------------------------------------------------------------------------\nprint all lines                              ==> pyp  "pp"\nsort all input lines                         ==> pyp  "pp.sort()"\neliminate duplicates                         ==> pyp  "pp.uniq()"\ncombine all lines to one line                ==> pyp  "pp.oneline()"\nprint line after FOO                         ==> pyp  "pp.after(\'FOO\')"\nlist comprehenision                          ==> pyp  "[x for x in pp]"\nreturn to string context after sort          ==> pyp  "pp.sort() | p"\n\n-------------------------------------------------------------------------------\n            String Operations               # all python str methods work\n-------------------------------------------------------------------------------\nprint line                                   ==> pyp  "p"\ncombine line with FOO                        ==> pyp  "p +\'FOO\'"\nabove, but combine with original input       ==> pyp  "p +\'FOO\'| p + o"\n\nreplace FOO with GOO                         ==> pyp  "p.replace(\'FOO\',\'GOO\')"\nremove all GOO and FOO                       ==> pyp  "p.kill(\'GOO\',\'FOO\')"\n\nstring substitution                          ==> pyp  "\'%s FOO %s %s GOO\'%(p,p,5)"\n\nsplit up line by FOO                         ==> pyp  "p.split(\'FOO\')"\nsplit up line by \'/\'                         ==> pyp  "slash"\nselect 1st field split up by \'/\'             ==> pyp  "slash[0]"\nselect fields 3 through 5 split up by \'/\'    ==> pyp  "s[2:6]"   \nabove joined together with \'/\'               ==> pyp  "s[2:6] | s"\n\n-------------------------------------------------------------------------------\n            Logic Filters                   # all python Booleon methods work\n-------------------------------------------------------------------------------\nkeep all lines with GOO and FOO              ==> pyp  "\'GOO\' in p and \'FOO\' in p"\nkeep all lines with GOO or FOO               ==> pyp  "keep(\'GOO\',\'FOO\')"\nkeep all lines that are numbers              ==> pyp  "p.isdigit()"\n\nlose all lines with GOO and FOO              ==> pyp  "\'GOO\' not in p and \'FOO\' not in p"\nlose all lines with GOO or FOO               ==> pyp  "lose(\'GOO\',\'FOO\')"\nlose all lines that are numbers              ==> pyp  "not p.isdigit()"\n\n-------------------------------------------------------------------------------                \nTO SEE EXTENDED HELP, use --manual\n\n'
def main():
	global options,args,Colors,pyp;parser=optparse.OptionParser(Docs.usage);parser.add_option('-m','--manual',action='store_true',help='prints out extended help');parser.add_option('-l','--macro_list',action='store_true',help='lists all available macros');parser.add_option('-s','--macro_save',dest='macro_save_name',type='string',help='saves current command as macro. use "#" for adding comments  EXAMPLE:    pyp -s "great_macro # prints first letter" "p[1]"');parser.add_option('-f','--macro_find',dest='macro_find_name',type='string',help='searches for macros with keyword or user name');parser.add_option('-d','--macro_delete',dest='macro_delete_name',type='string',help='deletes specified public macro');parser.add_option('-g','--macro_group',action='store_true',help='specify group macros for save and delete; default is user');parser.add_option('-t','--text_file',type='string',help='specify text file to load. for advanced users, you should typically cat a file into pyp');parser.add_option('-x','--execute',action='store_true',help='execute all commands.');parser.add_option('-c','--turn_off_color',action='store_true',help='prints raw, uncolored output');parser.add_option('-u','--unmodified_config',action='store_true',help='prints out generic PypCustom.py config file');parser.add_option('-b','--blank_inputs',action='store',type='string',help="generate this number of blank input lines; useful for generating numbered lists with variable 'n'");parser.add_option('-n','--no_input',action='store_true',help='use with command that generates output with no input; same as --dummy_input 1');parser.add_option('-k','--keep_false',action='store_true',help='print blank lines for lines that test as False. default is to filter out False lines from the output');parser.add_option('-r','--rerun',action='store_true',help='rerun based on automatically cached data from the last run. use this after executing "pyp", pasting input into the shell, and hitting CTRL-D');options,args=parser.parse_args()
	if options.turn_off_color or options.execute:Colors=NoColors
	try:pyp=Pyp().main()
	except Exception as err:print(Colors.RED+str(err)+Colors.OFF)
if __name__=='__main__': main()