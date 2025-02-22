<template>
  <div>
    <div class="trash__title">
      <div class="trash__title-left">
        <h2 class="trash__title-heading">{{ title }}</h2>
        <div class="trash__title-description">
          Restore deleted items from the past {{ trashDuration }}
        </div>
      </div>
      <div class="trash__title-right">
        <a
          v-show="totalServerSideTrashContentsCount > 0 && !parentIsTrashed"
          class="button button--error"
          :disabled="loadingContents"
          @click="showEmptyModalIfNotLoading"
          >{{ emptyButtonText }}</a
        >
      </div>
    </div>
    <div v-if="loadingContents" class="loading-overlay"></div>
    <div
      v-else-if="totalServerSideTrashContentsCount === 0"
      class="trash__empty"
    >
      <i class="trash__empty-icon fas fa-recycle"></i>
      <div class="trash__empty-text">
        Nothing has been deleted in the past three days.
      </div>
    </div>
    <div v-else class="trash__entries">
      <InfiniteScroll
        :max-count="totalServerSideTrashContentsCount"
        :current-count="trashContents.length"
        @load-next-page="$emit('load-next-page', $event)"
      >
        <TrashEntry
          v-for="item in trashContents"
          :key="'trash-item-' + item.id"
          :trash-entry="item"
          :disabled="loadingContents || shouldTrashEntryBeDisabled(item)"
          @restore="$emit('restore', $event)"
        ></TrashEntry>
        <div v-if="loadingNextPage" class="trash__entries-loading-wrapper">
          <div class="loading"></div>
        </div>
      </InfiniteScroll>
    </div>
    <TrashEmptyModal
      ref="emptyModal"
      :name="title"
      :loading="loadingContents"
      :selected-is-trashed="selectedItem.trashed"
      @empty="$emit('empty')"
    ></TrashEmptyModal>
  </div>
</template>

<script>
/**
 * Displays a infinite scrolling list of trash contents for either a selectedTrashGroup or
 * a specific selectedTrashApplication in the selectedTrashGroup. The user can empty the trash
 * contents permanently deleting them all, or restore individual trashed items.
 *
 * If the selectedItem (the selectedTrashApplication if provided, otherwise the selectedTrashGroup
 * ) is trashed itself then the modal will display buttons and modals which indicate
 * that they will permanently delete the selectedItem instead of just emptying it's
 * contents.
 */

import moment from 'moment'
import TrashEntry from '@baserow/modules/core/components/trash/TrashEntry'
import InfiniteScroll from '@baserow/modules/core/components/infinite_scroll/InfiniteScroll'
import TrashEmptyModal from '@baserow/modules/core/components/trash/TrashEmptyModal'

export default {
  name: 'TrashContents',
  components: { InfiniteScroll, TrashEntry, TrashEmptyModal },
  mixins: [],
  props: {
    selectedTrashGroup: {
      type: Object,
      required: true,
    },
    selectedTrashApplication: {
      type: Object,
      required: false,
      default: null,
    },
    trashContents: {
      type: Array,
      required: true,
    },
    loadingContents: {
      type: Boolean,
      required: true,
    },
    loadingNextPage: {
      type: Boolean,
      required: true,
    },
    totalServerSideTrashContentsCount: {
      type: Number,
      required: true,
    },
  },
  computed: {
    parentIsTrashed() {
      return (
        this.selectedTrashApplication !== null &&
        this.selectedTrashGroup.trashed
      )
    },
    selectedItem() {
      return this.selectedTrashApplication === null
        ? this.selectedTrashGroup
        : this.selectedTrashApplication
    },
    selectedItemType() {
      return this.selectedTrashApplication === null ? 'Group' : 'Application'
    },
    title() {
      const title = this.selectedItem.name
      return title === ''
        ? `Unnamed ${this.selectedItemType} ${this.selectedItem.id}`
        : title
    },
    emptyButtonText() {
      if (this.selectedItem.trashed) {
        return `Delete ${this.selectedItemType} permanently`
      } else {
        return `Empty this ${this.selectedItemType}'s trash`
      }
    },
    trashDuration() {
      const hours = this.$env.HOURS_UNTIL_TRASH_PERMANENTLY_DELETED
      return moment().subtract(hours, 'hours').fromNow().replace('ago', '')
    },
  },
  methods: {
    showEmptyModalIfNotLoading() {
      if (!this.loadingContents) {
        this.$refs.emptyModal.show()
      }
    },
    shouldTrashEntryBeDisabled(entry) {
      const selectedItemType = this.selectedItemType.toLowerCase()
      const entryIsForSelectedItem =
        entry.trash_item_id === this.selectedItem.id &&
        entry.trash_item_type === selectedItemType
      return (
        this.parentIsTrashed ||
        (this.selectedItem.trashed && !entryIsForSelectedItem)
      )
    },
  },
}
</script>
