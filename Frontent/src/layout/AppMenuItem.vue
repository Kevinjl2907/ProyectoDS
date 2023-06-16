<script setup>
import { ref, onBeforeMount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useLayout } from '@/layout/composables/layout';

const route = useRoute();

const { layoutConfig, layoutState, setActiveMenuItem, onMenuToggle, isHorizontal, isSlim, isDesktop } = useLayout();

const props = defineProps({
    item: {
        type: Object,
        default: () => ({})
    },
    index: {
        type: Number,
        default: 0
    },
    root: {
        type: Boolean,
        default: true
    },
    parentItemKey: {
        type: String,
        default: null
    }
});

const isActiveMenu = ref(false);
const itemKey = ref(null);

onBeforeMount(() => {
    itemKey.value = props.parentItemKey ? props.parentItemKey + '-' + props.index : String(props.index);

    const activeItem = layoutState.activeMenuItem.value;

    isActiveMenu.value = activeItem === itemKey.value || activeItem ? activeItem.startsWith(itemKey.value + '-') : false;
});

watch(
    () => layoutState.activeMenuItem.value,
    (newVal) => {
        isActiveMenu.value = newVal === itemKey.value || newVal.startsWith(itemKey.value + '-');
    }
);

watch(
    () => layoutConfig.menuMode.value,
    () => {
        isActiveMenu.value = false;
    }
);

watch(
    () => layoutState.overlaySubmenuActive.value,
    (newValue) => {
        if (!newValue) {
            isActiveMenu.value = false;
        }
    }
);
watch(
    () => route.path,
    (newPath) => {
        if (!(isSlim.value || isHorizontal.value) && props.item.to && props.item.to === newPath) {
            setActiveMenuItem(itemKey);
        } else if (isSlim.value || isHorizontal.value) {
            isActiveMenu.value = false;
        }
    }
);
const itemClick = async (event, item) => {
    if (item.disabled) {
        event.preventDefault();
        return;
    }

    const { overlayMenuActive, staticMenuMobileActive } = layoutState;

    if ((item.to || item.url) && (staticMenuMobileActive.value || overlayMenuActive.value)) {
        onMenuToggle();
    }

    if (item.command) {
        item.command({ originalEvent: event, item: item });
    }

    if (item.items) {
        if (props.root && isActiveMenu.value && (isSlim.value || isHorizontal.value)) {
            layoutState.overlaySubmenuActive.value = false;
            layoutState.menuHoverActive.value = false;

            return;
        }

        setActiveMenuItem(isActiveMenu.value ? props.parentItemKey : itemKey);

        if (props.root && !isActiveMenu.value && (isSlim.value || isHorizontal.value)) {
            layoutState.overlaySubmenuActive.value = true;
            layoutState.menuHoverActive.value = true;
            isActiveMenu.value = true;

            removeAllTooltips();
        }
    } else {
        if (!isDesktop) {
            layoutState.staticMenuMobileActive.value = !layoutState.staticMenuMobileActive.value;
        }

        if (isSlim.value || isHorizontal.value) {
            layoutState.overlaySubmenuActive.value = false;
            layoutState.menuHoverActive.value = false;

            return;
        }

        setActiveMenuItem(itemKey);
    }
};

const onMouseEnter = () => {
    if (props.root && (isSlim.value || isHorizontal.value) && isDesktop) {
        if (!isActiveMenu.value && layoutState.menuHoverActive.value) {
            setActiveMenuItem(itemKey);
        }
    }
};
const removeAllTooltips = () => {
    const tooltips = document.querySelectorAll('.p-tooltip');
    tooltips.forEach((tooltip) => {
        tooltip.remove();
    });
};
const checkActiveRoute = (item) => {
    return route.path === item.to;
};
</script>

<template>
    <li :class="{ 'layout-root-menuitem': root, 'active-menuitem': isActiveMenu }">
        <div v-if="root && item.visible !== false" class="layout-menuitem-root-text">{{ item.label }}</div>
        <a
            v-if="(!item.to || item.items) && item.visible !== false"
            :href="item.url"
            @click="itemClick($event, item, index)"
            :class="item.class"
            :target="item.target"
            tabindex="0"
            @mouseenter="onMouseEnter"
            v-tooltip.hover="isSlim && root && !isActiveMenu ? item.label : null"
        >
            <i :class="item.icon" class="layout-menuitem-icon"></i>
            <span class="layout-menuitem-text">{{ item.label }}</span>
            <i class="pi pi-fw pi-angle-down layout-submenu-toggler" v-if="item.items"></i>
        </a>
        <router-link
            v-if="item.to && !item.items && item.visible !== false"
            @click="itemClick($event, item, index)"
            :class="[item.class, { 'active-route': checkActiveRoute(item) }]"
            tabindex="0"
            :to="item.to"
            @mouseenter="onMouseEnter"
            v-tooltip.hover="isSlim && root && !isActiveMenu ? item.label : null"
        >
            <i :class="item.icon" class="layout-menuitem-icon"></i>
            <span class="layout-menuitem-text">{{ item.label }}</span>
            <i class="pi pi-fw pi-angle-down layout-submenu-toggler" v-if="item.items"></i>
        </router-link>

        <ul v-if="item.items && item.visible !== false">
            <app-menu-item v-for="(child, i) in item.items" :key="child" :index="i" :item="child" :parentItemKey="itemKey" :root="false"></app-menu-item>
        </ul>
    </li>
</template>
