<div dir="rtl" align="right">

# طریقه استفاده از برنامه

این پروژه به علت استفاده در پروژه GED شامل فایل‌های متعددی می‌باشد اما برای استخراج گراف واژگان فقط از دو فایل زیر استفاده می‌کنیم:
<div  dir="ltr"  align="left">
 
 - src/generate_bipartite_from_input.py
 - src/readBipartiteAndCommunityDetection.py
</div>
ابتدا با دستور زیر، پیش‌نیازهای برنامه را نصب می‌کنیم:

<div  dir="ltr"  align="left">

    pip install -r requirements.txt
</div>

سپس با دو روش زیر فایل generate_bipartite_from_input.py را اجرا می‌کنیم:

 

 1. از طریق IDE فایل را مستقیم اجرا می‌کنیم
 2. از طریق cmd با دستور زیر اجرا می‌کنیم:
 <div  dir="ltr"  align="left">
 
 `python -m src.generate_bipartite_from_input`
 
 </div>





سپس با وارد کردن نام استاد، اطلاعات استاد از پایگاه داده فراخوانی شده و فایل graphml و خروجی svg ساخته می‌شود:

![enter image description here](./assets/project1.PNG)

حال برای اجتماع‌یابی، فایل readBipartiteAndCommunityDetection.py را به یکی از دو صورت بالا اجرا می‌کنیم و نام فایل graphml ساخته شده در مرحله قبل را وارد می‌کنیم:

![enter image description here](./assets/project2.PNG)
