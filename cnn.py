#手写数字识别，两个卷积层加一个全连接层
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)
sees = tf.InteractiveSession()

#设置权重和偏置
def weight_variable(shape):
    initial = tf.truncated_normal(shape,stddev=0.1)#加随机噪声
    return tf.Variable(initial)

def bais_variable(shape):
    initial = tf.constant(0.1,shape=shape)#避免死亡节点
    return tf.Variable(initial)

#定义卷积层和池化层
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
#二维卷积函数，x输入，W卷积的参数，SAME给边界加上padding，让卷积的输入和输出保持同样尺寸
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#需要
x=tf.placeholder(tf.float32,[None,784])
y_=tf.placeholder(tf.float32,[None,10])
x_image = tf.reshape(x,[-1,28,28,1])

W_conv1 = weight_variable([5,5,1,32])#卷积核尺寸5*5,1个颜色通道，32个不同卷积核
b_conv1 = bais_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)#conv2d函数进行卷积操作，加上偏置，再用relu激活函数进行激活
h_pool1 = max_pool_2x2(h_conv1)#池化

#第二个卷积层
W_conv2 = weight_variable([5,5,32,64])#卷积核尺寸5*5,1个颜色通道，32个不同卷积核
b_conv2 = bais_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)#conv2d函数进行卷积操作，加上偏置，再用relu激活函数进行激活
h_pool2 = max_pool_2x2(h_conv2)#池化

#定义全连接层
W_fc1 = weight_variable([7*7*64,1024])
b_fc1 = bais_variable([1024])
h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)

#dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

W_fc2 = weight_variable([1024,10])
b_fc2 = bais_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)

#定义损失函数 cross entropy
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y_conv),reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

#训练
tf.global_variables_initializer().run()
for i in range(20000):#初始训练20000次
    batch = mnist.train.next_batch(50)
    if i%100==0:
        train_accuracy = accuracy.eval(feed_dict={x:batch[0],y_:batch[1],keep_prob:1.0})
        print("step %d ,training accuracy %g"%(i,train_accuracy))
    train_step.run(feed_dict={x:batch[0],y_:batch[1],keep_prob:0.5})

#测试集
#print("test accuracy%g"% accuracy.eval(feed_dict={x:mnist.test.images,y_:mnist.test.labels,keep_prob:1.0}))

a = 10
b = 50
sum = 0
for i in range(a):
    testSet = mnist.test.next_batch(b)
    c = accuracy.eval(feed_dict={x: testSet[0], y_: testSet[1], keep_prob: 1.0})
    sum += c * b
    #print("test accuracy %g" %  c)
print("test accuracy %g" %  (sum / (b * a)))


