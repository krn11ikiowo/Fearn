//
//  ColorPickerView.swift
//  NexStore
//
//  Created by Cascade on 6/15/26.
//

import SwiftUI

struct ColorPickerView: View {
    @Binding var selectedColor: String
    let onColorSelected: (String) -> Void
    
    @State private var tempColor: Color = Color(hex: "#3482c9")
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            Form {
                Section {
                    ColorPicker(
                        "Custom Accent Color",
                        selection: $tempColor,
                        supportsOpacity: false
                    )
                } header: {
                    Text("Choose your custom accent color")
                } footer: {
                    Text("This color will be used throughout the app for accents, buttons, and highlights.")
                }
                
                Section {
                    HStack {
                        Text("Selected Color")
                        Spacer()
                        Circle()
                            .fill(tempColor)
                            .frame(width: 30, height: 30)
                    }
                    
                    HStack {
                        Text("Hex Value")
                        Spacer()
                        Text(tempColor.toHex() ?? selectedColor)
                            .foregroundColor(.secondary)
                    }
                }
            }
            .navigationTitle("Custom Color")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        if let hex = tempColor.toHex() {
                            selectedColor = hex
                            onColorSelected(hex)
                        }
                        dismiss()
                    }
                    .fontWeight(.semibold)
                }
            }
        }
        .onAppear {
            tempColor = Color(hex: selectedColor)
        }
    }
}

// MARK: - Color Extensions
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }
        
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
    
    func toHex() -> String? {
        guard let components = UIColor(self).cgColor.components, components.count >= 3 else {
            return nil
        }
        
        let r = Float(components[0])
        let g = Float(components[1])
        let b = Float(components[2])
        
        return String(format: "#%02lX%02lX%02lX",
                      lroundf(r * 255),
                      lroundf(g * 255),
                      lroundf(b * 255))
    }
}
