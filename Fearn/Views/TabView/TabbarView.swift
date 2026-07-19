//
//  TabbarView.swift
//  Feather
//
//  Created by samara on 11.04.2025.
//

import SwiftUI
import NukeUI

struct TabbarView: View {
	@State private var selectedTab: TabEnum = .appstore
	@Environment(\.horizontalSizeClass) var horizontalSizeClass

	var body: some View {
		ZStack(alignment: .bottom) {
			// Main content
			TabView(selection: $selectedTab) {
				ForEach(TabEnum.defaultTabs, id: \.self) { tab in
					TabEnum.view(for: tab)
						.tag(tab)
				}
			}
			.tabViewStyle(.page(indexDisplayMode: .never))
			.padding(.bottom, 100)

			// Custom bottom tab bar
			VStack {
				Spacer()
				CustomTabBar(selectedTab: $selectedTab, tabs: TabEnum.defaultTabs)
					.padding(.horizontal, 20)
					.padding(.bottom, 20)
			}
		}
	}
}

struct CustomTabBar: View {
	@Binding var selectedTab: TabEnum
	let tabs: [TabEnum]
	@State private var tabPositions: [CGFloat] = []
	
	var body: some View {
		HStack(spacing: 0) {
			ForEach(Array(tabs.enumerated()), id: \.element) { index, tab in
				Button {
					withAnimation(.spring(response: 0.4, dampingFraction: 0.7)) {
						selectedTab = tab
					}
				} label: {
					VStack(spacing: 4) {
						ZStack {
							// Icon
							Image(systemName: tab.icon)
								.font(.system(size: 22, weight: selectedTab == tab ? .semibold : .regular))
								.foregroundStyle(selectedTab == tab ? Color.accentColor : .secondary)
								.scaleEffect(selectedTab == tab ? 1.1 : 1.0)
								.animation(.spring(response: 0.3, dampingFraction: 0.6), value: selectedTab)
						}
						.frame(height: 32)
						
						// Label
						Text(tab.title)
							.font(.system(size: 10, weight: selectedTab == tab ? .semibold : .regular))
							.foregroundStyle(selectedTab == tab ? Color.accentColor : .secondary)
							.lineLimit(1)
							.minimumScaleFactor(0.8)
					}
					.frame(maxWidth: .infinity)
					.contentShape(Rectangle())
				}
				.buttonStyle(PlainButtonStyle())
				.background(
					GeometryReader { geometry in
						Color.clear.preference(key: TabPositionKey.self, value: [index: geometry.frame(in: .global).midX])
					}
				)
			}
		}
		.padding(.horizontal, 8)
		.padding(.vertical, 12)
		.background(
			RoundedRectangle(cornerRadius: 24)
				.fill(.ultraThinMaterial)
		)
		.clipShape(RoundedRectangle(cornerRadius: 24))
		.onPreferenceChange(TabPositionKey.self) { positions in
			self.tabPositions = positions.sorted { $0.key < $1.key }.map { $0.value }
		}
		.overlay(
			// Animated indicator
			GeometryReader { geometry in
				if let selectedIndex = tabs.firstIndex(where: { $0 == selectedTab }),
				   selectedIndex < tabPositions.count {
					Capsule()
						.fill(Color.accentColor.opacity(0.2))
						.frame(width: 40, height: 4)
						.position(x: tabPositions[selectedIndex], y: geometry.size.height - 2)
						.animation(.spring(response: 0.4, dampingFraction: 0.7), value: selectedTab)
				}
			}
		)
	}
}

struct TabPositionKey: PreferenceKey {
	static var defaultValue: [Int: CGFloat] = [:]
	
	static func reduce(value: inout [Int: CGFloat], nextValue: () -> [Int: CGFloat]) {
		value.merge(nextValue(), uniquingKeysWith: { $1 })
	}
}
