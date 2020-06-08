```javascript
// Loop through the opening documents, two each group. 

// This assumes that all open documents are 12" wide.
// 1. Resize the first document's canvas to the right by 12".
// 2. Copy the next document into the white space (12", 0)
// 3. Close next document.
var groups = app.documents.length / 2;

for(var idx = 0; idx < groups; idx++) {
  // Step 1
  app.activeDocument = app.documents[2 * idx];
  app.activeDocument.flatten();
  app.activeDocument.resizeCanvas("24in", activeDocument.height, AnchorPosition.MIDDLELEFT);
  
  var doc = app.activeDocument;
  var height = app.activeDocument.height.value;
  var width = app.activeDocument.width.value / 2; 
    
  // If there are odd number of documents, the last one will be extended to 24" by itself.
  if (2 * idx + 1 >= app.documents.length) {
    break;
  }
    
  // Step 2
  app.activeDocument = app.documents[2 * idx +1];
  app.activeDocument.flatten();
  app.activeDocument.artLayers["Background"].copy();
  
  app.activeDocument = app.documents[2 * idx];
  app.activeDocument.selection.select([
    [width, 0], 
    [width * 2, 0], 
    [width,height], 
    [width * 2, height]]);
  app.activeDocument.paste();
}

```
