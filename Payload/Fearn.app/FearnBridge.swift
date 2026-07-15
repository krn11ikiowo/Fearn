import Foundation
import UIKit

@objc public class FearnBridge: NSObject {
    @objc public static let shared = FearnBridge()
    
    @objc public func initializeNativeLayer() {
        print("Fearn Swift Native Bridge Layer Activated.")
    }
}
