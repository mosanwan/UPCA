slate_h_template =\
'#pragma once\n'\
'\n'\
'$authorinfo$\n'\
'\n'\
'class $API$ $classname$ : public SCompoundWidget\n'\
'{\n'\
'public:\n'\
'	SLATE_BEGIN_ARGS($classname$){}\n'\
'	SLATE_END_ARGS()\n'\
'\n'\
'	void Construct(const FArguments& InArgs);\n'\
'private:\n'\
'\n'\
'};'

slate_cpp_template = \
'#include "$pchfile$"\n'\
'#include "$classname$.h"\n'\
'\n'\
'#define  LOCTEXT_NAMESPACE "$classname$"\n'\
'\n'\
'void $classname$::Construct(const FArguments& InArgs)\n'\
'{\n'\
'	this->ChildSlot\n'\
'	[\n'\
'        SNew(SButton)\n'\
'	];\n'\
'}\n'\
'\n'\
'#undef   LOCTEXT_NAMESPACE'

user_ini_temp = \
'/**\n'\
'@ $classinfo$\n'\
'@Author $auhtorname$\n'\
'@Email  $authoremail$\n'\
'@Date   $time$\n'\
'\n'\
'$sign$\n'\
'*/\n'\