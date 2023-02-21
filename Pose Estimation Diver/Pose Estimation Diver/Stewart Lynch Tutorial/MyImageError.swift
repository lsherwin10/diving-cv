//
//  MyImageError.swift
//  Pose Estimation Diver
//
//  Created by Logan Sherwin on 9/18/22.
//

import SwiftUI

enum MyImageError: Error, LocalizedError {
    case readError
    case decodingError
    case encodingError
    case saveError
    case saveImageError
    case readImageError
    
    var errorDescription: String? {
        switch self {
            
        case .readError:
            return NSLocalizedString("Could not load MyImage.jsom, please reinstall the app.", comment: "")
        case .decodingError:
            return NSLocalizedString("There was a problem loading your list of images, please create a new image to start over.", comment: "")
        case .encodingError:
            return NSLocalizedString("Could not save your MyImage data, please reinstall the app.", comment: "")
        case .saveError:
            return NSLocalizedString("Could not save the MyImage json file, please reinstall the app.", comment: "")
        case .saveImageError:
            return NSLocalizedString("Could not save image, please reinstall the app.", comment: "")
        case .readImageError:
            return NSLocalizedString("Could not load image, please reinstall the app.", comment: "")
        }
    }
    
    struct ErrorType: Identifiable {
        let id = UUID()
        let error: MyImageError
        var message: String {
            error.localizedDescription
        }
        let button = Button("OK", role: .cancel) {}
    }
}
