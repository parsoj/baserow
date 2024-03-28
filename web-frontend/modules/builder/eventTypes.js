/**
 * This might look like something that belongs in a registry, but it does not.
 *
 * There is no point in making these accessible to plugin writers so there is no
 * registry required.
 */
export class Event {
  constructor({ i18n, store, registry }) {
    this.i18n = i18n
    this.store = store
    this.registry = registry
  }

  static getType() {
    throw new Error('getType needs to be implemented')
  }

  getType() {
    return this.constructor.getType()
  }

  get label() {
    return null
  }

  async fire({ workflowActions, applicationContext, resolveFormula }) {
    const additionalContext = {}
    for (let i = 0; i < workflowActions.length; i += 1) {
      const workflowAction = workflowActions[i]
      const workflowActionType = this.registry.get(
        'workflowAction',
        workflowAction.type
      )

      this.store.dispatch('workflowAction/setDispatching', {
        workflowAction,
        isDispatching: true,
      })
      try {
        additionalContext[workflowAction.id] = await workflowActionType.execute(
          {
            workflowAction,
            additionalContext,
            applicationContext,
            resolveFormula,
          }
        )
      } finally {
        this.store.dispatch('workflowAction/setDispatching', {
          workflowAction,
          isDispatching: false,
        })
      }
    }
  }
}

export class ClickEvent extends Event {
  static getType() {
    return 'click'
  }

  get label() {
    return this.i18n.t('eventTypes.clickLabel')
  }
}

export class SubmitEvent extends Event {
  static getType() {
    return 'submit'
  }

  get label() {
    return this.i18n.t('eventTypes.submitLabel')
  }
}

export class AfterLoginEvent extends Event {
  static getType() {
    return 'after_login'
  }

  get label() {
    return this.i18n.t('eventTypes.afterLoginLabel')
  }
}
