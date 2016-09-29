slate_h_template =\
'$authorinfo$\n'\
'\n'\
'#pragma once\n'\
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
'*/\n'

none_h_class = \
'$authorinfo$\n'\
'\n'\
'#pragma once\n'\
'\n'\
'class $API$ F$classname$ \n'\
'{\n'\
'public:\n'\
'\n'\
'private:\n'\
'\n'\
'};'

none_cpp_class_temp = \
'#include "$pchfile$"\n'\
'#include "$classname$.h"\n'\
'\n'

actor_h_class = \
'$authorinfo$\n'\
'\n'\
'#pragma once\n'\
'#include "$classname$.generated.h"\n'\
'\n'\
'UCLASS()\n'\
'class $API$ A$classname$ : public AActor\n'\
'{\n'\
'   $genera$()\n'\
'public:\n'\
'\n'\
'private:\n'\
'\n'\
'};'

actor_cpp_class = \
'#include "$pchfile$"\n'\
'#include "$classname$.h"\n'\
'\n'\
'A$classname$::A$classname$(const FObjectInitializer& ObjectInitializer)\n'\
':Super(ObjectInitializer)\n'\
'{\n'\
'\n'\
'}\n'

actor_cpp_class_none_construct = \
'#include "$pchfile$"\n'\
'#include "$classname$.h"\n'\
'\n'


object_h_class = \
'$authorinfo$\n'\
'\n'\
'#pragma once\n'\
'#include "$classname$.generated.h"\n'\
'\n'\
'UCLASS()\n'\
'class $API$ U$classname$ : public UObject\n'\
'{\n'\
'   $genera$()\n'\
'public:\n'\
'\n'\
'private:\n'\
'\n'\
'};'

object_cpp_class = \
'#include "$pchfile$"\n'\
'#include "$classname$.h"\n'\
'\n'\
'U$classname$::U$classname$(const FObjectInitializer& ObjectInitializer)\n'\
':Super(ObjectInitializer)\n'\
'{\n'\
'\n'\
'}\n'

object_cpp_class_none_construct = \
'#include "$pchfile$"\n'\
'#include "$classname$.h"\n'\
'\n'