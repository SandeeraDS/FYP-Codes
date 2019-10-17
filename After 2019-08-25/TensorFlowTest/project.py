import tensorflow as tf


intNum1 = 10
intNum2 = 20

num1 = tf.Variable(intNum1)
num2 = tf.Variable(intNum2)

sum = tf.add(num1, num2)

print("sum - "+str(sum))
