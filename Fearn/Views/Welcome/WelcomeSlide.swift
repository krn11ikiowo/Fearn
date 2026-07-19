//
//  WelcomeSlide.swift
//  NexStore
//
//  Created by Cascade on 16.06.2026.
//

import SwiftUI

// MARK: - Model
struct WelcomeSlide: Identifiable {
    let id = UUID()
    let title: String
    let subtitle: String
    let iconName: String
    let isIconSelectionSlide: Bool
    
    init(title: String, subtitle: String, iconName: String, isIconSelectionSlide: Bool = false) {
        self.title = title
        self.subtitle = subtitle
        self.iconName = iconName
        self.isIconSelectionSlide = isIconSelectionSlide
    }
}
