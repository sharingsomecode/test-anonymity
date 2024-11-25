# test-anonymity
This pygame-based code produces an interactive interface that allows to present movies in random order, and with various quality levels. The original goal was to test whether participants could identify the persons in the movie.

# content
This release contains
- the python code producing the interface
- a zip file containing examples of movies for 2 passages (each back and forth) of the same person under the kinect camera. Each movie is provided with 8 levels of quality. These movies are only provided for code testing. They are not meant to be used for research.

# install
Some parameters must be adjusted in the python code.
In particular:
- the path for the directory containing the movies;
- the path for the directory where results will be stored;
- the number of movies 'nbf' you have (without distinguishing quality level).
If you use the movies we provide, then nbf must be set equal to 2.

Run the code with python3:

python3 testanonymity.py

