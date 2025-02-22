<template>
  <Modal :sidebar="true" :full-height="true">
    <template #sidebar>
      <TrashSidebar
        v-if="!loading"
        :groups="groups"
        :selected-trash-group="selectedTrashGroup"
        :selected-trash-application="selectedTrashApplication"
        @selected="selectGroupOrApp"
      ></TrashSidebar>
    </template>
    <template #content>
      <div v-if="loading" class="loading-absolute-center"></div>
      <div v-else-if="groups.length === 0" class="placeholder">
        <div class="placeholder__icon">
          <i class="fas fa-layer-group"></i>
        </div>
        <h1 class="placeholder__title">No groups found</h1>
        <p class="placeholder__content">
          You aren't a member of any group. Applications like databases belong
          to a group, so in order to create them you need to create a group.
        </p>
      </div>
      <TrashContent
        v-else
        :selected-trash-group="selectedTrashGroup"
        :selected-trash-application="selectedTrashApplication"
        :trash-contents="trashContents"
        :loading-contents="loadingContents"
        :loading-next-page="loadingNextPage"
        :total-server-side-trash-contents-count="
          totalServerSideTrashContentsCount
        "
        @empty="onEmpty"
        @restore="onRestore"
        @load-next-page="loadNextPage"
      ></TrashContent>
    </template>
  </Modal>
</template>

<script>
import { mapState } from 'vuex'

import modal from '@baserow/modules/core/mixins/modal'
import { notifyIf } from '@baserow/modules/core/utils/error'
import TrashService from '@baserow/modules/core/services/trash'
import TrashSidebar from '@baserow/modules/core/components/trash/TrashSidebar'
import TrashContent from '@baserow/modules/core/components/trash/TrashContents'

export default {
  name: 'TrashModal',
  components: { TrashSidebar, TrashContent },
  mixins: [modal],
  props: {
    initialGroup: {
      type: Object,
      required: false,
      default: null,
    },
    initialApplication: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      loading: true,
      loadingContents: true,
      loadingNextPage: false,
      groups: [],
      trashContents: [],
      selectedTrashGroup: null,
      selectedTrashApplication: null,
      totalServerSideTrashContentsCount: 0,
    }
  },
  computed: {
    ...mapState({
      selectedGroup: (state) => state.group.selected,
      selectedApplication: (state) => state.application.selected,
    }),
  },
  methods: {
    /**
     * Chooses which group to show when the modal is shown.
     **/
    pickInitialGroupToSelect() {
      // The initial or selected groups will not contain the trashed flag as they so
      // we must look them up in the groups fetched from the trash api.
      const initialGroupWithTrashInfo = this.initialGroup
        ? this.groups.find((i) => i.id === this.initialGroup.id)
        : null
      const selectedGroupWithTrashInfo = this.selectedGroup
        ? this.groups.find((i) => i.id === this.selectedGroup.id)
        : null
      return (
        initialGroupWithTrashInfo ||
        selectedGroupWithTrashInfo ||
        this.groups[0] || // When all groups are trashed we want to pick the first one.
        null
      )
    },
    /**
     * Chooses which app to show when the modal is shown.
     **/
    pickInitialApplicationToSelect(firstGroupToShow) {
      if (firstGroupToShow === null) {
        return null
      } else {
        // The initial or selected apps will not contain the trashed flag as they so
        // we must look them up in the groups fetched from the trash api.
        const applications = firstGroupToShow.applications
        if (this.initialApplication || this.initialGroup) {
          // When either of the initial props are set we have been opened via a context
          // menu shortcut.
          return this.initialApplication
            ? applications.find((i) => i.id === this.initialApplication.id)
            : null
        } else {
          return this.selectedApplication
            ? applications.find((i) => i.id === this.selectedApplication.id)
            : null
        }
      }
    },
    /**
     * Loads the structure of the trash modal from the server, selects an initial
     * group or application depending on the props and shows the trash modal.
     **/
    async show(...args) {
      modal.methods.show.call(this, ...args)

      this.loading = true
      this.groups = []
      this.selectedTrashGroup = null
      this.selectedTrashApplication = null

      try {
        const { data } = await TrashService(this.$client).fetchStructure()
        this.groups = data.groups
        const initialGroup = this.pickInitialGroupToSelect()
        await this.selectGroupOrApp({
          group: initialGroup,
          application: this.pickInitialApplicationToSelect(initialGroup),
        })
      } catch (error) {
        notifyIf(error, 'trash')
        this.hide()
      }
      this.loading = false
    },
    /**
     * Loads the next page of trash contents for the currently selected application.
     */
    async loadTrashContentsPage(nextPage) {
      if (
        this.selectedTrashGroup === null &&
        this.selectedTrashApplication === null
      ) {
        return
      }
      try {
        const { data } = await TrashService(this.$client).fetchContents({
          page: nextPage,
          groupId: this.selectedTrashGroup.id,
          applicationId:
            this.selectedTrashApplication !== null
              ? this.selectedTrashApplication.id
              : null,
        })
        this.totalServerSideTrashContentsCount = data.count
        data.results.forEach((entry) => {
          entry.loading = false
          this.trashContents.push(entry)
        })
      } catch (error) {
        notifyIf(error, 'trash')
      }
    },
    /**
     * Switches to a different group or application to display the trash contents for
     * and triggers the fetch for the first page of contents.
     */
    async selectGroupOrApp({ group, application = null }) {
      this.selectedTrashGroup = group
      this.selectedTrashApplication = application
      this.loadingContents = true
      this.trashContents = []
      this.totalServerSideTrashContentsCount = 0
      await this.loadTrashContentsPage(1)
      this.loadingContents = false
    },
    /**
     * Loads another page of contents in after we have already loaded the initial
     * page of contents, hence we want to use a different loading indicator as it is
     * ok to say, restore an item whilst we are loading in another page.
     */
    async loadNextPage(nextPage) {
      this.loadingNextPage = true
      await this.loadTrashContentsPage(nextPage)
      this.loadingNextPage = false
    },
    /**
     * Triggered when a user requests a trashEntry be restored. Sends the request to
     * the server, updates the client side state if successful and updates the trash
     * structure if say a group or application was restored.
     */
    async onRestore(trashEntry) {
      try {
        trashEntry.loading = true
        await TrashService(this.$client).restore({
          trash_item_type: trashEntry.trash_item_type,
          trash_item_id: trashEntry.trash_item_id,
          parent_trash_item_id: trashEntry.parent_trash_item_id,
        })
        const index = this.trashContents.findIndex(
          (t) => t.id === trashEntry.id
        )
        this.trashContents.splice(index, 1)
        this.totalServerSideTrashContentsCount--
        this.updateStructureIfGroupOrAppRestored(trashEntry)
      } catch (error) {
        notifyIf(error, 'trash')
      }
      trashEntry.loading = false
    },
    updateStructureIfGroupOrAppRestored(trashEntry) {
      /**
       * If a group or app is trashed it is displayed with a strike through it's text.
       * This method checks if a restored trash entry is a group or application and
       * if so updates the state of said group/app so it no longer is displayed as
       * trashed.
       */
      const trashItemId = trashEntry.trash_item_id
      const trashItemType = trashEntry.trash_item_type
      if (trashItemType === 'group') {
        const index = this.groups.findIndex((group) => group.id === trashItemId)
        this.groups[index].trashed = false
      } else if (trashItemType === 'application') {
        const index = this.selectedTrashGroup.applications.findIndex(
          (app) => app.id === trashItemId
        )
        this.selectedTrashGroup.applications[index].trashed = false
      }
    },
    /**
     * Triggered when the user has requested the currently selected group or app
     * should be emptied. If the selected item is trashed itself the empty operation
     * will permanently delete the selected item also. Once emptied this method will
     * ensure that any now permanently deleted groups or apps are removed from the
     * sidebar.
     */
    async onEmpty() {
      this.loadingContents = true
      try {
        const applicationIdOrNull =
          this.selectedTrashApplication !== null
            ? this.selectedTrashApplication.id
            : null
        await TrashService(this.$client).emptyContents({
          groupId: this.selectedTrashGroup.id,
          applicationId: applicationIdOrNull,
        })
        this.removeGroupOrAppFromSidebarIfNowPermDeleted()
        this.trashContents = []
        this.totalServerSideTrashContentsCount = 0
      } catch (error) {
        notifyIf(error, 'trash')
      }
      this.loadingContents = false
    },
    removeSelectedAppFromSidebar() {
      const applicationId = this.selectedTrashApplication.id

      const indexToDelete = this.selectedTrashGroup.applications.findIndex(
        (app) => app.id === applicationId
      )
      this.selectedTrashGroup.applications.splice(indexToDelete, 1)
      if (this.selectedTrashGroup.applications.length > 0) {
        this.selectedTrashApplication = this.selectedTrashGroup.applications[0]
      } else {
        this.selectedTrashApplication = null
      }
    },
    removeSelectedTrashGroupFromSidebar() {
      const indexToDelete = this.groups.findIndex(
        (group) => group.id === this.selectedTrashGroup.id
      )
      this.groups.splice(indexToDelete, 1)
      if (this.groups.length > 0) {
        this.selectedTrashGroup = this.groups[0]
      } else {
        this.selectedTrashGroup = null
      }
    },
    /**
     * Updates the trash structure to remove any deleted groups or applications after
     * an empty is performed.
     */
    removeGroupOrAppFromSidebarIfNowPermDeleted() {
      if (
        this.selectedTrashApplication !== null &&
        this.selectedTrashApplication.trashed
      ) {
        this.removeSelectedAppFromSidebar()
        this.selectGroupOrApp({
          group: this.selectedTrashGroup,
          application: this.selectedTrashApplication,
        })
      } else if (this.selectedTrashGroup.trashed) {
        this.removeSelectedTrashGroupFromSidebar()
        this.selectGroupOrApp({
          group: this.selectedTrashGroup,
          application: this.selectedTrashApplication,
        })
      } else if (this.selectedTrashApplication === null) {
        // The group was emptied, it might have contained trashed applications hence
        // we need to search through the trash and remove any now deleted applications.
        for (const app of this.selectedTrashGroup.applications.slice()) {
          if (app.trashed) {
            const index = this.selectedTrashGroup.applications.findIndex(
              (i) => i.id === app.id
            )
            this.selectedTrashGroup.applications.splice(index, 1)
          }
        }
      }
    },
  },
}
</script>
