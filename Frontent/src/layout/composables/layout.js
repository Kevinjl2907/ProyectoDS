import { toRefs, reactive, computed } from 'vue';

const contextPath = import.meta.env.BASE_URL;

const layoutConfig = reactive({
    ripple: false,
    inputStyle: 'outlined',
    menuMode: 'horizontal',
    menuTheme: 'primaryColor',
    colorScheme: 'light',
    theme: 'indigo',
    scale: 14
});

const layoutState = reactive({
    staticMenuDesktopInactive: false,
    overlayMenuActive: false,
    overlaySubmenuActive: false,
    profileSidebarVisible: false,
    configSidebarVisible: false,
    staticMenuMobileActive: false,
    menuHoverActive: false,
    activeMenuItem: null
});

export function useLayout() {
    const setScale = (scale) => {
        layoutConfig.scale = scale;
    };

    const setActiveMenuItem = (item) => {
        layoutState.activeMenuItem = item.value || item;
    };

    const onMenuToggle = () => {
        if (layoutConfig.menuMode === 'overlay') {
            layoutState.overlayMenuActive = !layoutState.overlayMenuActive;
        }

        if (window.innerWidth > 991) {
            layoutState.staticMenuDesktopInactive = !layoutState.staticMenuDesktopInactive;
        } else {
            layoutState.staticMenuMobileActive = !layoutState.staticMenuMobileActive;
        }
    };

    const onProfileSidebarToggle = () => {
        layoutState.profileSidebarVisible = !layoutState.profileSidebarVisible;
    };

    const isSidebarActive = computed(() => layoutState.overlayMenuActive || layoutState.staticMenuMobileActive || layoutState.overlaySubmenuActive);

    const isDarkTheme = computed(() => true);

    const isDesktop = computed(() => window.innerWidth > 991);

    const isSlim = computed(() => layoutConfig.menuMode === 'slim');
    const isHorizontal = computed(() => layoutConfig.menuMode === 'horizontal');

    return { contextPath, layoutConfig: toRefs(layoutConfig), layoutState: toRefs(layoutState), setScale, onMenuToggle, isSidebarActive, isDarkTheme, setActiveMenuItem, onProfileSidebarToggle, isSlim, isHorizontal, isDesktop };
}
