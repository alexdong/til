# Vision Network - Still Image Analysis

## Saliency

Objectness Saliency is trained on object segmentation. VN will return no more
than 3 regions.  It can be used to segment and focus on different part of the
image. This would improve the quality of the classification process.  This is
similar to the "Focus" mode of visual processing. 

Attention Saliency is trained on eye tracking data. So there is always only one
saliency region. What's cool about it is that it contains motion data.  So use
Attention Saliency for optimal content-aware cropping. 

Given that Attention Saliency has only one region. If a photo has two people
sitting on each side of a table, the *joint* region will make up of the entire
image, whereas Objectness Saliency will be more appropriate. 

The mask is a bitmap with float values from 0 to 1. It can be used to
selectively run certain filters on an image. 


## Classification

VN has a [taxonomy of 1303
classifications](https://gist.github.com/alexdong/5da51b09d4fc07139f6ce98ceb8705ab).
Its classification operation will return an score for each classification.

VN has applied a TF/IDF-like approach to the taxonomy. This *relative
significance* of each classification is reflected in the precision/recall
parameter for each classfication. By specifying a range for both parameters, VN
will automatically explore and converge on the possible value.

For example, in `{ $0.hasMinimumPrecision(0.0, forRecall: 0.7) }`, even if
there is no convergent point on the P/R curve, VN will figure out the best
option for us. 


## Feature print

Feature print is like having a word vector for each photo that describes the
content of the photo. My initial thought was that it's basically a vector of
the classification results. But apparently its 2048, instead of 1303, features
that Apple's deep neural network has identified as the most salient *descriptors* in
distinguishing one photo from another. These features probably don't make any
sense to a human, but they are what Apple's DNN thinks is the most important
dimensions. 


## Face capture quality

This quality only makes sense across photos of the same subject. It's a
comparative measure. The absolute value does not convey any meaning. 
