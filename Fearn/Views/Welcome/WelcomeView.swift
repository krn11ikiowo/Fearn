//
//  WelcomeView.swift
//  NexStore
//
//  Created by Cascade on 16.06.2026.
//

import SwiftUI

// MARK: - View
struct WelcomeView: View {
    @State private var currentIndex: Int = 0
    @State private var selectedIcon: String? = UIApplication.shared.alternateIconName
    
    // Easy to add new slides - just add to this array
    private let slides: [WelcomeSlide] = [
        WelcomeSlide(
            title: "Welcome to NexStore",
            subtitle: "The best all-in-one app for sideloading on iOS",
            iconName: "app.badge.fill"
        ),
        WelcomeSlide(
            title: "Choose Your Icon",
            subtitle: "Personalize your experience with a custom app icon",
            iconName: "paintbrush.fill",
            isIconSelectionSlide: true
        ),
        WelcomeSlide(
            title: "You're All Set!",
            subtitle: "Start exploring and enjoy your NexStore experience",
            iconName: "checkmark.circle.fill"
        )
    ]
    
    private let appIcons: [AppIconOption] = [
        AppIconOption(
            id: "primary",
            title: "Default",
            subtitle: "NexStore",
            iconName: "AppIcon",
            alternateIconName: nil
        ),
        AppIconOption(
            id: "wave",
            title: "Wave",
            subtitle: "Ocean Blue",
            iconName: "AppIcon-Wave-Preview",
            alternateIconName: "AppIcon-Wave"
        ),
    ]
    
    var body: some View {
        VStack(spacing: 0) {
            // Progress indicator
            HStack {
                ForEach(0..<slides.count, id: \.self) { index in
                    Capsule()
                        .fill(index <= currentIndex ? Color.accentColor : Color.gray.opacity(0.3))
                        .frame(height: 4)
                        .animation(.easeInOut, value: currentIndex)
                }
            }
            .padding(.horizontal, 40)
            .padding(.top, 20)
            
            // Slide content
            TabView(selection: $currentIndex) {
                ForEach(Array(slides.enumerated()), id: \.element.id) { index, slide in
                    VStack(spacing: 30) {
                        Spacer()
                        
                        // Title and subtitle
                        VStack(spacing: 12) {
                            Text(slide.title)
                                .font(.largeTitle)
                                .fontWeight(.bold)
                                .multilineTextAlignment(.center)
                            
                            Text(slide.subtitle)
                                .font(.body)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 40)
                        }
                        
                        // Icon
                        if slide.isIconSelectionSlide {
                            _iconSelectionContent
                        } else {
                            Image(systemName: slide.iconName)
                                .font(.system(size: 80))
                                .foregroundColor(.accentColor)
                        }
                        
                        Spacer()
                        
                        // Navigation buttons
                        _navigationButtons(for: index)
                    }
                    .tag(index)
                }
            }
            .tabViewStyle(.page(indexDisplayMode: .never))
            .animation(.easeInOut, value: currentIndex)
        }
        .background(Color(UIColor.systemBackground))
    }
}

// MARK: - View extension
extension WelcomeView {
    @ViewBuilder
    private var _iconSelectionContent: some View {
        ScrollView {
            VStack(spacing: 16) {
                ForEach(appIcons, id: \.id) { iconOption in
                    _iconCell(for: iconOption)
                }
            }
            .padding(.horizontal, 20)
        }
        .frame(height: 200)
    }
    
    @ViewBuilder
    private func _iconCell(for iconOption: AppIconOption) -> some View {
        Button {
            _changeAppIcon(to: iconOption)
        } label: {
            HStack(spacing: 12) {
                if let image = UIImage(named: iconOption.iconName) ?? UIImage(named: Bundle.main.iconFileName ?? "") {
                    Image(uiImage: image)
                        .appIconStyle(size: 60)
                } else {
                    Image("App_Unknown")
                        .appIconStyle(size: 60)
                }
                
                VStack(alignment: .leading, spacing: 2) {
                    Text(iconOption.title)
                        .font(.headline)
                        .foregroundColor(.primary)
                    Text(iconOption.subtitle)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                if selectedIcon == iconOption.alternateIconName {
                    Image(systemName: "checkmark")
                        .foregroundColor(.accentColor)
                        .font(.headline)
                }
            }
            .contentShape(Rectangle())
            .padding(.vertical, 8)
            .padding(.horizontal, 12)
            .background(Color(UIColor.secondarySystemBackground))
            .cornerRadius(12)
        }
        .buttonStyle(.plain)
    }
    
    @ViewBuilder
    private func _navigationButtons(for index: Int) -> some View {
        HStack(spacing: 16) {
            // Back button (except on first slide)
            if index > 0 {
                Button {
                    withAnimation {
                        currentIndex -= 1
                    }
                } label: {
                    Text("Back")
                        .font(.headline)
                        .foregroundColor(.accentColor)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.accentColor.opacity(0.1))
                        .cornerRadius(12)
                }
            }
            
            // Next/Done button
            if index < slides.count - 1 {
                Button {
                    withAnimation {
                        currentIndex += 1
                    }
                } label: {
                    Text("Next")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.accentColor)
                        .cornerRadius(12)
                }
            } else {
                Button {
                    _completeWelcome()
                } label: {
                    Text("Done")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.accentColor)
                        .cornerRadius(12)
                }
            }
        }
        .padding(.horizontal, 40)
        .padding(.bottom, 40)
    }
    
    private func _changeAppIcon(to iconOption: AppIconOption) {
        guard selectedIcon != iconOption.alternateIconName else { return }
        
        UIApplication.shared.setAlternateIconName(iconOption.alternateIconName) { error in
            DispatchQueue.main.async {
                if let error = error {
                    print("Failed to change app icon: \(error.localizedDescription)")
                } else {
                    self.selectedIcon = iconOption.alternateIconName
                    print("Successfully changed app icon to: \(iconOption.alternateIconName ?? "primary")")
                }
            }
        }
    }
    
    private func _completeWelcome() {
        UserDefaults.standard.set(true, forKey: "hasCompletedWelcome")
    }
}