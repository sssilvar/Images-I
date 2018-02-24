import tensorflow as tf

# Print Version
print(tf.__version__)

# Say Hello world!
hello = tf.constant('Hello World')

with tf.Session() as sess:
    result = sess.run(hello)

print(result)

# Operations
a = tf.constant(10)
b = tf.constant(20)

with tf.Session() as sess:
    result = sess.run(a + b)

print('Adding result: %d' % result)

# Some other type of vars
const = tf.constant(10)
fill_mat = tf.fill((4, 4), 10)
zeros_mat = tf.zeros((4, 4))
ones_mat = tf.ones((4, 4))
normal_dist_mat = tf.random_normal((4, 4), mean=0, stddev=1.0)
uniform_dist_mat = tf.random_uniform((4, 4), minval=0, maxval=1)

my_ops = [const, fill_mat, zeros_mat, ones_mat, zeros_mat, normal_dist_mat, uniform_dist_mat]

sess = tf.InteractiveSession()
for op in my_ops:
    print(op.eval())
    print('\n')
