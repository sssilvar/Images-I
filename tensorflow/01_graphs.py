import tensorflow as tf

n1 = tf.constant(10)
n2 = tf.constant(20)

# Adder node
n3 = n1 + n2

# Run process
with tf.Session() as sess:
    result = sess.run(n3)

print(result)
