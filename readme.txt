项目名称：Handwritten-Digit-Recognition-Based-on-Correlation-and-Discrimination

项目目的：因为在学习communication System第5周内容的时候接触到了Auto-correlation和Corss-correlation。在发现在一维的状态下可以使连续超长信号中查找相对应的同步码进行比较。利用Discrimination进行得到峰值，实现数字的区分和识别

项目原理：在学习材料中提到R(k)=Σ x[n] · y[n-k] 其中目的是做卷积，将x信号不动，y信号每次左移得到积，将所有积相加得到R,利用R(0)/|R(K)|得到D，D就是区分度。但是发现在2维信号中把左移k的地方改成上下左右挪动（rx和ry），在2维状态下使用Corss-correlation得到25组RxyK,将1-9之间的25组进行对比得出最大值，最大值就是相似度，相似度越高越接近。

发现问题：在制作好基本原理后发现识别误差很大（详细请参考Cross-Correlation.py和identify.py）所以在基础上增加了NCC去除利用偏移rx和ry后添加的白色和黑色之间产生的平均值移除白色背景的偏差 公式：((Black*1)+((400-Black)*-1))/400 400是因为识别的图片大小为20x20pix，原本使用的大小是10x10,但是在调整偏差的时候发现图像大小对于识别并没有多少用处。虽然利用公式去除白色背景干扰但是最后发现new = Moving_Data(C_data_L, dx, dy)
C_ave = aveList(C_data_L)中aveList函数输入的值还是原本没被移动的值，所以结论是使用C_data_L的成功率高于new。这是一个很奇怪的现象