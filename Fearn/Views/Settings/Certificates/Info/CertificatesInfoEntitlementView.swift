//
//  CertificatesInfoEntitlementView.swift
//  Feather
//
//  Created by samara on 27.04.2025.
//

import SwiftUI
import NimbleViews

// MARK: - View
struct CertificatesInfoEntitlementView: View {
	let entitlements: [String: AnyCodable]
	
	// MARK: Body
	var body: some View {
		let booleanKeys = entitlements.keys.filter { entitlements[$0]?.value is Bool }.sorted()
		let otherKeys = entitlements.keys.filter { !(entitlements[$0]?.value is Bool) }.sorted()
		
		NBList(.localized("Entitlements")) {
			ForEach(booleanKeys, id: \.self) { key in
				if let value = entitlements[key]?.value {
					CertificatesInfoEntitlementCellView(key: key, value: value)
				}
			}
			
			if !otherKeys.isEmpty && !booleanKeys.isEmpty {
				Section {
					EmptyView()
				} header: {
					EmptyView()
				}
			}
			
			ForEach(otherKeys, id: \.self) { key in
				if let value = entitlements[key]?.value {
					CertificatesInfoEntitlementCellView(key: key, value: value)
				}
			}
		}
		.listStyle(.grouped)
	}
}
