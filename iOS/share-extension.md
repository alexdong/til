## Concepts

### Hosting app, container app and extension

Share extension supports both iOS and macOS. Each extension is a separate binary
that runs independent of the app used to deliver it.

An app that contains one or more extensions is called a containing app. You
create an app extension by adding a new target to an app.

To distribute app extensions to users, you submit a containing app to the App
Store.  When a user installs your containing app, the extensions it contains are
also installed.  After installing an app extension, a user must take action to
enable it.

An app that a user employs to choose an app extension is called a host app. A
host app defines the context provided to the extension and kicks off the
extension life cycle when it sends a request in response to a user action. An
extension typically terminates soon after it completes the request it received
from the host app.

There is no direct communication between an app extension and its containing
app; typically, the containing app isn’t even running while a contained
extension is running. An app extension’s containing app and the host app don’t
communicate at all.

Any app extension and its containing app can access shared data in a privately
defined shared container.


### Background upload using `NSURLSession` and shared container

In iOS, your app extension might need a bit more time to complete a potentially
lengthy task, such as uploading content to a website. When this is the case, you
can use the `NSURLSession` class to initiate a transfer in the background.
Because a background transfer uses a separate process, the transfer can
continue, as a low priority task, after your extension completes the host app’s
request and gets terminated.

If your app extension initiates a background NSURLSession task, you must also
set up a shared container that both the extension and its containing app can
access. Use the sharedContainerIdentifier` property of the
`NSURLSessionConfiguration` class to specify an identifier for the shared
container so that you can access it later. 

```objc
   NSURLSession *mySession = [self configureMySession];
   NSURL *url = [NSURL URLWithString:@"http://www.example.com/LargeFile.zip"];
   NSURLSessionTask *myTask = [mySession downloadTaskWithURL:url];
   [myTask resume];

- (NSURLSession *) configureMySession {
    if (!mySession) {
      NSURLSessionConfiguration* config = [NSURLSessionConfiguration backgroundSessionConfigurationWithIdentifier:@“com.mycompany.myapp.backgroundsession”];
      // To access the shared container you set up, use the sharedContainerIdentifier property on your configuration object.
      config.sharedContainerIdentifier = @“com.mycompany.myappgroupidentifier”;
      mySession = [NSURLSession sessionWithConfiguration:config delegate:self delegateQueue:nil];
    }
    return mySession;
}
```

Because only one process can use a background session at a time, you need to
create a different background session for the containing app and each of its app
extensions. (Each background session should have a unique identifier.) It’s
recommended that your containing app only use a background session that was
created by one of its extensions when the app is launched in the background to
handle events for that extension. If you need to perform other network-related
tasks in your containing app, create different URL sessions for them.

In iOS, if your extension isn’t running when a background task completes, the
system launches your containing app in the background and calls the
`application:handleEventsForBackgroundURLSession:completionHandler:` app
delegate method.


Use data sharing to share data between the extension and the containing app.
This is done through the App Group. After you enable app groups, an app
extension and its containing app can both use the `NSUserDefaults` API to share
access to user preferences. To enable this sharing, use the `initWithSuiteName:`
method to instantiate a new NSUserDefaults object, passing in the identifier of
the shared group. 

```objc
// Create and share access to an NSUserDefaults object
NSUserDefaults *mySharedDefaults = [[NSUserDefaults alloc] initWithSuiteName: @"nz.happymoose.upload-extension"];

// Use the shared user defaults object to update the user's account
[mySharedDefaults setObject:theAccountName forKey:@"knownAPIKey"];
```


### Framework and key function calls

A Share extension uses its principal view controller’s `extensionContext`
property to get the `NSExtensionContext` object that contains the user’s initial
text and any attachments for a post, such as links, images, or videos.

Your app extension doesn’t own the main run loop, so it’s crucial that you
follow the established rules for good behavior in main run loops. For example,
if your extension blocks the main run loop, it can create a bad user
experience in another extension or app.

All completion blocks used in the NSItemProvider class are called by the system
on an internal queue. Ensure that user-interface updates take place on the main
queue as follows:
```swift
DispatchQueue.main.async {
    // work that impacts the user interface
}
```

An app extension typically encounters item providers when examining the
attachments property of an NSExtensionItem object. During that examination, the
extension can use the `hasItemConformingToTypeIdentifier("public.image")` method
to look for data that it recognizes. ("public.image") is the UTI of image type.

Get the context and items in your view controller’s loadView method so that you
can display the information in your view.

```objc
NSExtensionContext *myExtensionContext = self.extensionContext;
NSArray *inputItems = myExtensionContext.inputItems;
```

We can use
[`NSItemProvider.loadPreviewImage`](https://developer.apple.com/documentation/foundation/nsitemprovider/1403925-loadpreviewimage)
to show the first N images the customer has selected. We can also use the
preview image to indicate the file we are currently uploading.



### Development, debugging and profiling

The scheme in an Xcode app extension template uses the Ask On Launch option for
the executable. With this option, each time you build and run your project
you’re prompted to pick a host app. If you want to instead specify a particular
host to use every time, open the scheme editor and use the Info tab for the app
extension scheme’s Run phase.

Because app extensions must be responsive and efficient, it's a good idea to
watch the debug gauges in the debug navigator while you're running your
extension. The debug gauges show how your extension uses the CPU, memory, and
other system resources while it runs. If you see evidence of performance
problems, such as an unusual spike in CPU usage, you can use Instruments to
profile your extension and identify areas for improvement. You can open
Instruments while you’re in a debugging session by clicking Profile in
Instruments in any debug gauge report (to view a debug gauge report, click the
gauge in the debug area).

You can create an embedded framework to share code between your app extension
and its containing app. For example, if you develop an image filter for use in
your Photo Editing extension as well as in its containing app, put the filter’s
code in a framework and embed the framework in both targets.


### Deployment and Release

To pass app review, your containing app must provide functionality to users; it
can’t just contain app extensions. What shall we do? Everyday book creator?
Classic prints? Retro prints? The goal is to keep the scope really tight.

An app extension target must include the `arm64` (iOS) or `x86_64` architecture
(OS X) in its Architectures build settings or it will be rejected by the App
Store. Xcode includes the appropriate 64-bit architecture with its “Standard
architectures” setting when you create a new app extension target.

## TODO

[] Create container app
  [] Container app as a "Library viewer"
  [] Xcode share template
  [] declare supported data types for a Share Extension via `Info.plist` 
  [] `NSExtensionActivationRule` -> `NSExtensionActivationSupportsImageWithMaxCount`
  [] `NSExtensionPointIdentifier`-> `nz.happymoose.upload-services` 
  [] Share option show up in Action Sheet
[] Compose view controller (system provided or completely custom)
  [] Show logo and brand name.
  [] Show total number of photos to be uploaded. 
  [] Background upload and show results in the container app.
  [] Upload to HappyMoose API
[] Authentication through the container app. Sign in with Apple through the [AuthenticationServices](https://developer.apple.com/documentation/authenticationservices/implementing_user_authentication_with_sign_in_with_apple).
  [] Once authenticated through the website, store the API key with container and make it available to the extension.

## References

### Documentations
* [App Extension Essentials](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/index.html#//apple_ref/doc/uid/TP40014214-CH20-SW1)
* [Share
Extension](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/Share.html#//apple_ref/doc/uid/TP40014214-CH12-SW1)

### APIs

* [NSExtensionContext](https://developer.apple.com/documentation/foundation/nsextensioncontext),
[`.inputItems`](https://developer.apple.com/documentation/foundation/nsextensioncontext/1414827-inputitems)
* [NSExtensionItem](https://developer.apple.com/documentation/foundation/nsextensionitem),
[`.attachments`](https://developer.apple.com/documentation/foundation/nsextensionitem/1416690-attachments) and
[NSItemProvider](https://developer.apple.com/documentation/foundation/nsitemprovider)
* [Uniform Type Identifier (UTI)](https://developer.apple.com/library/archive/documentation/General/Conceptual/DevPedia-CocoaCore/UniformTypeIdentifier.html)
* [`URLSession uploadTask(with:fromFile:)`](https://developer.apple.com/documentation/foundation/urlsession/1411550-uploadtask)

### Tutorial and Examples

* [imgurShare](https://www.appcoda.com/ios8-share-extension-swift/)
* [JellyFish](https://www.jellyfishtechnologies.com/blog/share-extension-ios-swift/)
* [InstaPaper Share](https://github.com/oguzbilgener/SendToInstapaper/blob/master/ShareExtension/SendingViewController.swift)
* [Share inspector](https://github.com/cocologics/ShareInspector)
