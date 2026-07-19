//
//  TabEnum.swift
//  feather
//
//  Created by samara on 22.03.2025.
//

import SwiftUI
import NimbleViews

enum TabEnum: String, CaseIterable, Hashable {
    case files
	case library
	case settings
	case certificates
	case appstore
	var title: String {
		switch self {
        case .files:        return .localized("Files")
		case .library: 		return .localized("My Apps")
		case .settings: 	return .localized("Settings")
		case .certificates:	return .localized("Certificates")
		case .appstore: 	return .localized("App Store")
		}
	}
	
	var icon: String {
		switch self {
        case .files:        return "folder.fill"
		case .library: 		return "square.grid.2x2"
		case .settings: 	return "gearshape"
		case .certificates: return "person.text.rectangle"
		case .appstore: 	return "cart.fill"
		}
	}
	
	@ViewBuilder
	static func view(for tab: TabEnum) -> some View {
		switch tab {
        case .files: FilesView()
		case .library: LibraryView()
		case .settings: SettingsView()
		case .certificates: CertificatesView()
		case .appstore: AppstoreView()
		}
	}
	
	static var defaultTabs: [TabEnum] {
		return [
            .appstore,
            .library,
            .certificates,
            .files,
			.settings,
		]
	}
	
	static var customizableTabs: [TabEnum] {
		return []
	}
}
