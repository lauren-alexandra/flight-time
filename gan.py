#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout, BatchNormalization, Activation, ZeroPadding2D, UpSampling2D, Conv2D, LeakyReLU
from tensorflow.keras.optimizers import Adam, SGD

"""
A GAN model for image synthesis trained using the CIFAR-10 dataset.
"""

""" load the data """ 

# CIFAR10 data 

(X, y), (_, _) = tf.keras.datasets.cifar10.load_data()

# select a single class of images
# the number was randomly chosen and any number between 1 and 10 can be chosen

X = X[y.flatten() == 8]

""" define parameters """

image_shape = (32, 32, 3) # defining the Input shape
latent_dimensions = 100

""" a utility function to build the generator """

def build_generator(): 

    model = tf.keras.Sequential()

    # build the input layer
    model.add(Dense(128 * 8 * 8, activation="relu",

                    input_dim=latent_dimensions))

    model.add(Reshape((8, 8, 128)))         

    model.add(UpSampling2D())          

    model.add(Conv2D(128, kernel_size=3, padding="same"))

    model.add(BatchNormalization(momentum=0.78))

    model.add(Activation("relu"))          

    model.add(UpSampling2D())          

    model.add(Conv2D(64, kernel_size=3, padding="same"))

    model.add(BatchNormalization(momentum=0.78))

    model.add(Activation("relu"))          

    model.add(Conv2D(3, kernel_size=3, padding="same"))

    model.add(Activation("tanh"))

    # generate the output image

    noise = Input(shape=(latent_dimensions,))
    image = model(noise)  

    return tf.keras.Model(noise, image)

""" a utility function to build the discriminator """

def build_discriminator():

    # build the convolutional layers to classify whether an image is real or fake

    model = tf.keras.Sequential()

    model.add(Conv2D(32, kernel_size=3, strides=2,

                        input_shape=image_shape, padding="same"))

    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))

    model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))

    model.add(ZeroPadding2D(padding=((0,1),(0,1))))

    model.add(BatchNormalization(momentum=0.82))

    model.add(LeakyReLU(alpha=0.25))

    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))

    model.add(BatchNormalization(momentum=0.82))

    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))

    model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))

    model.add(BatchNormalization(momentum=0.8))

    model.add(LeakyReLU(alpha=0.25))

    model.add(Dropout(0.25))

    # build the output layer

    model.add(Flatten())

    model.add(Dense(1, activation='sigmoid'))
  
    image = Input(shape=image_shape)
    validity = model(image)

    return tf.keras.Model(image, validity)

""" a utility function to display the generated images """

def display_gen_images(epoch):

    r, c = 4,4
    noise = np.random.normal(0, 1, (r * c,latent_dimensions))
    generated_images = generator.predict(noise) 

    # scaling the generated images

    generated_images = 0.5 * generated_images + 0.5
    fig, axs = plt.subplots(r, c)
    count = 0

    for i in range(r):
        for j in range(c):
            axs[i,j].imshow(generated_images[count, :,:,])
            axs[i,j].axis('off')
            count += 1

    title = "Epoch_{}".format(epoch)
    filename = "{}.png".format(title)
    plt.title(title)
    plt.savefig(filename)
    plt.show()
    plt.close()

""" a utility function to plot the losses from the discriminator and the generator """

def plot_losses(losses_discm, losses_genr, epoch): 
    fig, axes = plt.subplots(1, 2, figsize=(8, 2))
    axes[0].plot(losses_discm)
    axes[1].plot(losses_genr)
    axes[0].set_title("losses_discm")
    axes[1].set_title("losses_genr")
    filename = "Losses_epoch_{}.png".format(epoch)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
    plt.close()

""" build the GAN """

# build and compile the discriminator

discriminator = build_discriminator()
discriminator.compile(loss='binary_crossentropy', optimizer=Adam(0.0002,0.5), metrics=['accuracy'])

# make the discriminator untrainable so that the generator can learn from fixed gradient

discriminator.trainable = False

# build the generator

generator = build_generator()

# define the input for the generator and generate the image

z = Input(shape=(latent_dimensions,))
image = generator(z)

# check the validity of the generated image

valid = discriminator(image) 

# define the combined model of the generator and the discriminator

combined_network = tf.keras.Model(z, valid)
combined_network.compile(loss='binary_crossentropy', optimizer=Adam(0.0002,0.5), metrics=['accuracy'])

""" train network """

num_epochs = 10000
display_interval = 500
last_epoch_tracked = num_epochs - 1
batch_size = 32
losses_discm = []
losses_genr = []

# normalize the input

X = (X / 127.5) - 1.     

# define the adversarial ground truths

valid = np.ones((batch_size, 1)) 

# add some noise 

valid += 0.05 * np.random.random(valid.shape)
fake = np.zeros((batch_size, 1))
fake += 0.05 * np.random.random(fake.shape)

for epoch in range(num_epochs):             

    # train the discriminator

    # sample a random half of images

    index = np.random.randint(0, X.shape[0], batch_size)
    images = X[index] 

    # sample noise and generating a batch of new images
    noise = np.random.normal(0, 1, (batch_size, latent_dimensions))
    generated_images = generator.predict(noise)          

    # train the discriminator to detect more accurately whether a generated image is real or fake

    discm_loss_real = discriminator.train_on_batch(images, valid)
    discm_loss_fake = discriminator.train_on_batch(generated_images, fake)
    discm_loss = 0.5 * np.add(discm_loss_real, discm_loss_fake)
    losses_discm.append(discm_loss)

    # train the generator

    # train the generator to generate images that pass the authenticity test

    genr_loss = combined_network.train_on_batch(noise, valid)
    losses_genr.append(genr_loss)

    # track the progress                

    if (epoch % display_interval == 0) or (epoch == last_epoch_tracked):
        display_gen_images(epoch)
        plot_losses(losses_discm, losses_genr, epoch)
        print("epoch={}, loss_discm={}, loss_genr={}".format(epoch, discm_loss, genr_loss))
