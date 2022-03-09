<h1>Statistical Analysis and Unsupervised Clustering of Asian Art in American Museums</h1>
<h4>Jenny Sheng</h4>
<h4>Princeton University Class of 2022</h4>
<h4>Advised by Professor Brian Kernighan</h4>
<p>Within the past five years, there have been increasing interest in the idea of collections as data. Collections as data is this concept of treating cultural heritage collections as datasets that can also be examined statistically and computationally. It is part of a movement to expand the spheres of cultural heritage analysis from careful scrutinization to large scale computation and research. In response to this idea, museums have also made much effort toward making their artwork data publicly available in bulk. For instance, the Getty adopted an Open Content Program in order to make their artwork images available to researchers. Numerous other museums have started to make their data be open access to the public under the Creative Common Zero license (CC0).</p>
<p>However, as these changes take place and museum collections become increasingly accessible, there have been surprisingly few efforts and attempts to examine these data together as a whole. Museums represent the cultural landscapes of the world. They are not only windows into the past and present, but also tell interesting tales of curatorial trends, public interest in specific spheres of art, cultural representation, provenance representation, etc. Yet, none of these trends can be confidently examined just by considering one specific collection. There is definitely more to the story when all these disparate museum collections are merged together to create a holistic view.</p>
<p>The goal of our project is to examine the intersection of Asian art between different museums and find commonalities and differences across museum collections in order to gain a better understanding of the Asian art collection in the United States. The project has three major components. First, through rectification and merging of museum metadata, we explored the statistical relationships between museum artwork acquisition across the curatorial landscape. Second, through unsupervised clustering of museum images, we probed into the visual similarities of artworks across datasets. Third, we created a web application that offers a variety of features to support users pursing similar projects. In this project, we focus on the following five museum datasets: Princeton University Art Museum (PUAM), The Metropolitan Museum of Art (MET), Museum of Modern Art (MOMA), Carnegie Museum of Art (CMOA), and Minneapolis Institution of Art (MIA). </p>
<p>Please find the web application of this project at <a href="https://asian-art-in-american-museums.herokuapp.com/">https://asian-art-in-american-museums.herokuapp.com/</a> (The Similar Artwork Finder requires AWS S3 support. Unfortunately, I ran out of AWS credits, therefore that component is unavailable at the moment)</p>

<h3>Image Clustering Models</h3>
<p>Our implementation for the unsupervised clustering task utilized 10,000 images in total across the five datasets. We randomly sampled 2,000 images from MIA, PUAM, MET, MOMA, and CMOA. We did not choose to sample a certain percentage from each dataset because if we were to take this approach, there would have been serious skewness of data from a single dataset. For instance, the Asian art collection at the MET was almost 11 times that of CMOA. We took a set number of images from each dataset in order to avoid this skewness of image data and to create an evenly distributed training set such that if there were significant clustering patterns with regard to repository, they would be easily recognizable. 2,000 was a number that was decided based on the computation limitations and storage limitations.</p>
<p>We used two different approaches to clustering and compared between the two. The first approach used the Keras model of the VGG16 network to extract feature vectors from the second-to-last fully connected layer `fc2'. The output of `fc2' has shape 1x4096 and is the default layer to choose when extracting features because it is the final layer before the prediction layer, so its vectors would contain all the key information. The feature vectors were then used for K-Means clustering. The second approach was to first train convolutional autoencoders on the training set. We then extracted features from the learned model for each training image to conduct K-Means clustering.</p>
<p>Please find the implementation code for image clustering in the "clustering" folder.</p>

<h3>Web application</h3>
<p>To make the merged Asian art dataset publicly accessible, as well as to create a simple interface that supports querying for specific fields, we created a web application for this project. The application has a HTML front end with Jinja and Bootstrap, a Flask backend coupled with scikit-learn and tensorflow to support the image similarity finder models, and a Postgres database. To achieve bulk storage of the 10,000 images needed for image clustering and to avoid hitting the Heroku memory limit, we used Amazon Simple Storage Service (Amazon S3) to store images as well as machine learning models. We also implemented automatic image tagging with Amazon Rekognition for all images. Please note that due to the rather big file sizes of all the models, the website takes longer than normal to load. </p>
<p>Please find the web application implementation code in the "museum-app" folder.</p>

<h3>Acknowledgements</h3>
<p>This project is a Spring 2021 independent work. Special thanks to Professor Brian Kernighan, Dr. Zoe LeBlanc, Vivien Nguyen, and my classmates in IW06 seminar for their help and support throughout this independent work.</p>
<p>Thank you to Princeton University Art Museum, The Metropolitan Museum of Art, Museum of Modern Art, Carnegie Museum of Art, and Minneapolis Institute of Art for making their museum data publicly available. Without their digital collections, this project would not have been possible.</p>
