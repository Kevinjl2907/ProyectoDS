<script setup>
import RadioButton from 'primevue/radiobutton';
import Button from 'primevue/button';
import InputSwitch from 'primevue/inputswitch';
import Sidebar from 'primevue/sidebar';
import PrimeVue from 'primevue/config';

import { ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';

const componentThemes = ref([
    { name: 'indigo', color: '#6366F1' },
    { name: 'blue', color: '#3B82F6' },
    { name: 'purple', color: '#8B5CF6' },
    { name: 'teal', color: '#14B8A6' },
    { name: 'cyan', color: '#06b6d4' },
    { name: 'green', color: '#10b981' },
    { name: 'orange', color: '#f59e0b' },
    { name: 'pink', color: '#d946ef' }
]);
const colorScheme = ref('light');

defineProps({
    simple: {
        type: Boolean,
        default: false
    }
});
const scales = ref([12, 13, 14, 15, 16]);
const visible = ref(false);

const { setScale, layoutConfig, layoutState } = useLayout();

watch(layoutConfig.menuMode, (newVal) => {
    if (newVal === 'static') {
        layoutState.staticMenuDesktopInactive.value = false;
    }
});

const onConfigButtonClick = () => {
    visible.value = !visible.value;
};
const changeColorScheme = (colorScheme) => {
    const themeLink = document.getElementById('theme-link');
    const themeLinkHref = themeLink.getAttribute('href');
    const currentColorScheme = 'theme-' + layoutConfig.colorScheme.value.toString();
    const newColorScheme = 'theme-' + colorScheme;
    const newHref = themeLinkHref.replace(currentColorScheme, newColorScheme);

    replaceLink(themeLink, newHref, () => {
        layoutConfig.colorScheme.value = colorScheme;
    });
};

const changeTheme = (theme) => {
    const themeLink = document.getElementById('theme-link');
    const themeHref = themeLink.getAttribute('href');
    const newHref = themeHref.replace(layoutConfig.theme.value, theme);

    replaceLink(themeLink, newHref, () => {
        layoutConfig.theme.value = theme;
    });
};

const replaceLink = (linkElement, href, onComplete) => {
    if (!linkElement || !href) {
        return;
    }

    const id = linkElement.getAttribute('id');
    const cloneLinkElement = linkElement.cloneNode(true);

    cloneLinkElement.setAttribute('href', href);
    cloneLinkElement.setAttribute('id', id + '-clone');

    linkElement.parentNode.insertBefore(cloneLinkElement, linkElement.nextSibling);

    cloneLinkElement.addEventListener('load', () => {
        linkElement.remove();

        const element = document.getElementById(id); // re-check
        element && element.remove();

        cloneLinkElement.setAttribute('id', id);
        onComplete && onComplete();
    });
};
const decrementScale = () => {
    setScale(layoutConfig.scale.value - 1);
    applyScale();
};
const incrementScale = () => {
    setScale(layoutConfig.scale.value + 1);
    applyScale();
};
const applyScale = () => {
    document.documentElement.style.fontSize = layoutConfig.scale.value + 'px';
};

const onChangeRipple = () => {
    PrimeVue.ripple = !PrimeVue.ripple;
};
</script>

<template>

    <Sidebar v-model:visible="visible" position="right" class="layout-config-sidebar w-20rem">
        <h5>Themes</h5>
        <div class="flex flex-wrap row-gap-3">
            <div v-for="(theme, i) in componentThemes" :key="i" class="w-3">
                <Button :autoFocus="layoutConfig.theme === theme.name" class="cursor-pointer p-link w-2rem h-2rem border-circle flex-shrink-0" @click="() => changeTheme(theme.name)" :style="{ 'background-color': theme.color }"></Button>
            </div>
        </div>

        <h5>Scale</h5>
        <div class="flex align-items-center">
            <Button icon="pi pi-minus" type="button" @click="decrementScale()" class="p-button-text p-button-rounded w-2rem h-2rem mr-2" :disabled="layoutConfig.scale.value === scales[0]"></Button>
            <div class="flex gap-2 align-items-center">
                <i class="pi pi-circle-fill text-300" v-for="s in scales" :key="s" :class="{ 'text-primary-500': s === layoutConfig.scale.value }"></i>
            </div>
            <Button icon="pi pi-plus" type="button" pButton @click="incrementScale()" class="p-button-text p-button-rounded w-2rem h-2rem ml-2" :disabled="layoutConfig.scale.value === scales[scales.length - 1]"></Button>
        </div>

        <template v-if="!simple">
            <h5>Menu Type</h5>
            <div class="field-radiobutton flex-1">
                <RadioButton name="menuMode" value="static" v-model="layoutConfig.menuMode.value" inputId="mode1"></RadioButton>
                <label for="mode1">Static</label>
            </div>

            <div class="field-radiobutton flex-1">
                <RadioButton name="menuMode" value="overlay" v-model="layoutConfig.menuMode.value" inputId="mode2"></RadioButton>
                <label for="mode2">Overlay</label>
            </div>
            <div class="field-radiobutton flex-1">
                <RadioButton name="menuMode" value="slim" v-model="layoutConfig.menuMode.value" inputId="mode3"></RadioButton>
                <label for="mode2">Slim</label>
            </div>
            <div class="field-radiobutton flex-1">
                <RadioButton name="menuMode" value="horizontal" v-model="layoutConfig.menuMode.value" inputId="mode2"></RadioButton>
                <label for="mode2">Horizontal</label>
            </div>

            <h5>Menu Theme</h5>
            <div class="field-radiobutton flex-1">
                <RadioButton :checked="layoutConfig.menuTheme === 'colorScheme'" name="menuTheme" value="colorScheme" v-model="layoutConfig.menuTheme.value" inputId="mode1"></RadioButton>
                <label for="mode1">Color Scheme</label>
            </div>

            <div class="field-radiobutton flex-1">
                <RadioButton :checked="layoutConfig.menuTheme === 'primaryColor'" name="menuTheme" value="primaryColor" v-model="layoutConfig.menuTheme.value" inputId="mode2"></RadioButton>
                <label for="mode2">Primary Color</label>
            </div>
            <div class="field-radiobutton flex-1">
                <RadioButton :checked="layoutConfig.menuTheme === 'transparent'" name="menuTheme" value="transparent" v-model="layoutConfig.menuTheme.value" inputId="mode3"></RadioButton>
                <label for="mode2">Transparent</label>
            </div>
        </template>

        <h5>Color Scheme</h5>
        <div class="field-radiobutton flex-1">
            <RadioButton v-model="colorScheme" name="colorScheme" value="light" @change="() => changeColorScheme('light')" inputId="outlined_input"></RadioButton>
            <label for="outlined_input">Light</label>
        </div>
        <div class="field-radiobutton flex-1">
            <RadioButton v-model="colorScheme" name="colorScheme" value="dim" @change="() => changeColorScheme('dim')" inputId="filled_input"></RadioButton>
            <label for="filled_input">Dim</label>
        </div>
        <div class="field-radiobutton flex-1">
            <RadioButton v-model="colorScheme" name="colorScheme" value="dark" @change="() => changeColorScheme('dark')" inputId="filled_input"></RadioButton>
            <label for="filled_input">Dark</label>
        </div>

        <template v-if="!simple">
            <h5>Input Style</h5>
            <div class="flex">
                <div class="field-radiobutton flex-1">
                    <RadioButton name="inputStyle" value="outlined" v-model="layoutConfig.inputStyle.value" inputId="outlined_input"></RadioButton>
                    <label for="outlined_input">Outlined</label>
                </div>
                <div class="field-radiobutton flex-1">
                    <RadioButton name="inputStyle" value="filled" v-model="layoutConfig.inputStyle.value" inputId="filled_input"></RadioButton>
                    <label for="filled_input">Filled</label>
                </div>
            </div>

            <h5>Ripple Effect</h5>
            <InputSwitch v-model="layoutConfig.ripple.value" @change="onChangeRipple"></InputSwitch>
        </template>
    </Sidebar>
</template>

<style lang="scss" scoped></style>

