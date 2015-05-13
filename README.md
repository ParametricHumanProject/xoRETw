## Synopsis

A database-driven webapp port of xoRET by Prof. Mark Strembeck - a role engineering tool for RBAC.

## Motivation

In the Parametric Human Project, data-sharing and collaboration between researchers are key features. 
Researchers may share medical imaging data, such as MRIs or CTs, or more general population data.
We began by trying to organize some of the main objects and control mechanisms and implemented a simple version of access control. 
However, it was not completely thought through and was based on some early assumptions. 
In restarting the thinking about this core issue, we discovered RBAC and a more formal methodology to design a solution. 
However, this also exposed the complexity of the task. Therefore, we sought out RBAC authoring tools to help us design our system. 
We found the open-source xoRET graphical software tool written in XOTcl but was not dynamic (i.e. database-driven). 
So, to help us (a) better understand RBAC, and (b) more toward a web-based tool for Parametric Human, 
we would like to begin by porting the xoRET tool to being a web-based database-driven tool that we call xoRETw. 

## Installation


## Tests


## Contributors


## License

xoRET

Copyright (C) 2003-2009 Mark Strembeck

Vienna University of Economics and Business
Institute of Information Systems / New Media Lab
Augasse 2-6, A-1090 Vienna, Austria
strembeck@{acm|computer}.org
     
Permission to use, copy, modify, distribute this software 
and its documentation for non-commercial purposes is hereby granted
without fee, provided that the above copyright notice appears in
all copies and modifications and that both that copyright notice and
this permission notice appear in supporting documentation. I make no
representations about the suitability of this software for any
purpose.  It is provided "as is" without express or implied
warranty.
