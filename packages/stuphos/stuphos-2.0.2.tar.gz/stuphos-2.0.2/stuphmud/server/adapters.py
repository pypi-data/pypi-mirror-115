# Adapter entity types.
from stuphos.triggers import EntityAdapter
from stuphos.triggers import TriggerAdapter
from stuphos.kernel import BypassReturn, vmCurrentTask

class InlineObject:
    def _getWrappedAttribute(self, name):
        # Asynchronous message passing of getattr to heartbeat.
        from world import heartbeat as vm
        task = vmCurrentTask()

        def getAttribute():
            vm.resumeTask(task, value = getattr(self._object, name))

        vm.suspendTask(task)
        vm.enqueueHeartbeatTask(getAttribute)

        raise BypassReturn


class PeerExtensionPoint(EntityAdapter):
    # {"valid",            (getter)peer_isvalid},
    # {"avatar",           (getter)peer_get_avatar},
    # {"original",         (getter)peer_get_original},
    # {"authority",        (getter)peer_get_authority},

    # // Functions as a method generator, too
    # {"state",            (getter)peer_get_state, (setter)peer_set_state},

    # {"input",            (getter)peer_get_next_command, (setter)peer_force_input},
    # {"large_outbuf",     (getter)peer_get_large_outbuf},

    # {"input_queue",      (getter)peer_get_input_block_queue},

    # // Use the output functions to change.
    # // {"output",           (getter)peer_get_output, (setter)peer_set_output},

    # {"echo",             (getter)NULL, (setter)peer_set_line_echo_state},
    # {"prompt",           (getter)peer_get_prompt},

    # {"interpreter",      (getter)peer_get_interpreter, (setter)peer_set_interpreter},
    # #if 0
    #     {"handler",          (getter)peer_get_interpreter, (setter)peer_set_interpreter},
    #     {"line_handler",     (getter)peer_get_interpreter, (setter)peer_set_interpreter},
    #     {"__interpreter__",  (getter)peer_get_interpreter, (setter)peer_set_interpreter},
    # #endif

    # {"olcmob", (getter)peer_get_edit_mob},
    # {"olcobj", (getter)peer_get_edit_obj},

    # #ifdef EXPOSE_DICT
    #     {"__dict__", (getter)peer_get_dict},
    # #endif

    # {"fileno", (getter)peer_get_fileno},
    # {"socket", (getter)peer_get_fileno},

    # {"network_mode", (getter)peer_get_network_mode, (setter)peer_set_network_mode},
    # {"networkMode",  (getter)getPeerNetworkMode,    (setter)setPeerNetworkMode   },

    # {"host",     (getter)peer_get_hostname, (setter)peer_set_hostname},
    # {"hostname", (getter)peer_get_hostname, (setter)peer_set_hostname},

    # MSTR(   last_host),
    # MSTR(  olc_string),
    # // MSTR(       inbuf),
    # MSTR(  last_input),
    # MSTR(small_outbuf),

    # // Fraun Sep 30th 2005 - Fixed these.  Was not T_STRING_INPLACE
    # M(email,  T_STRING, "email"),
    # M(remort, T_STRING, "remort"),

    # // See clear_output.
    # M(output, T_STRING, "output"),

    # MINT(  descriptor),
    # MINT(  ident_sock),
    # MINT(   peer_port),
    # MINT(          ip),
    # MINT(       login),
    # MINT(   connected),
    # MINT(    desc_num),
    # MINT(  login_time),
    # // MINT(     mail_to),
    # MINT(   mail_mode),
    # MINT(  has_prompt),
    # MINT(  color_mode),
    # MINT(  medit_mode),
    # MINT(  oedit_mode),
    # MINT(  sedit_mode),
    # MINT(  zedit_mode),
    # MINT(  zedit_page),
    # MINT( zedit_index),
    # MINT(  hedit_mode),
    # MINT(  cedit_mode),
    # MINT(   vt_bar_on),
    # MINT(       saved),
    # MINT(affect_index),
    # MINT(   edit_vnum),
    # MINT(   edit_room),
    # MINT(   edit_zone),
    # MINT(   edit_clan),
    # MINT(  help_entry),
    # MINT(   redit_dir),
    # MINT(  redit_mode),
    # MINT(     olc_int),
    # MINT( history_pos),
    # MINT(      bufptr),
    # MINT(    bufspace),

    # MINT(last_command_time),
    # MINT(    olc_save_type),
    # MINT(     bandwidth_in),
    # MINT(    bandwidth_out),

    # // Fraun Sep 30th 2005 - Not T_STRING_INPLACE
    # M(showstr_head,  T_STRING, "showstr_head"),
    # M(showstr_point, T_STRING, "showstr_point"),
    # M(showstr_start, T_STRING, "showstr_start"),

    # // $!@@# showstr_vector is (char **) !@#$@!
    # // MSTR(showstr_vector),

    # MINT( showstr_count),
    # // MINT(showstr_vector),
    # MINT(       max_str),

    # {"sendln", (PyCFunction)peer_sendln, METH_VARARGS,
    #  peer_sendln_doc},
    # {"textout", (PyCFunction)peer_textout, METH_VARARGS,
    #  peer_textout_doc},
    # {"write", (PyCFunction)peer_textout, METH_VARARGS,
    #  peer_textout_doc},

    # // Other Output Routines
    # {"page",         (PyCFunction)peer_page_string, METH_VARARGS, ""},
    # {"page_string",  (PyCFunction)peer_page_string, METH_VARARGS, ""},

    # {"clear_output", (PyCFunction)peer_clear_output, METH_NOARGS, "Reset the output buffers to contain nothing."},

    # // Functions as a getset getter, too
    # {"next_command", (PyCFunction)peer_get_next_command, METH_NOARGS, ""},

    # {"dequeue_input_block", (PyCFunction)peer_dequeue_input_block, METH_NOARGS, ""},

    # {"redirect", (PyCFunction)peer_redirect, METH_VARARGS, "A more broad/low-level form of intercepting output."},

    # {"members", (PyCFunction)peer_members, METH_NOARGS, ""},

    # {"string_edit", (PyCFunction)peerStringEdit, METH_VARARGS, ""},
    # {"editString",  (PyCFunction)peerStringEdit, METH_VARARGS, ""},

    # {"withdraw",    (PyCFunction)peerWithdraw,   METH_NOARGS,
    #  peerWithdrawDoc},
    # {"reload",      (PyCFunction)peerReload,     METH_VARARGS,
    #  peerReloadDoc},

    pass

PeerAdapter = PeerExtensionPoint

class MobileExtensionPoint(InlineObject, EntityAdapter):
    # {"peer", (getter)mobile_get_peer},
    # {"room", (getter)mobile_get_room, (setter)mobile_set_room},
    # {"location", (getter)mobile_get_room, (setter)mobile_set_room},
    # {"next", (getter)mobile_get_next},

    # {"zone", (getter)mobile_get_zone},

    # {"name",   (getter)mobile_get_name},
    # {"vnum",   (getter)mobile_get_vnum},

    # {"keywords", (getter)mobile_get_keywords, (setter)mobile_set_keywords},
    # {"short_descr", (getter)mobile_get_shortdescr, (setter)mobile_set_shortdescr},
    # {"long_descr", (getter)mobile_get_longdescr, (setter)mobile_set_longdescr},
    # {"description", (getter)mobile_get_description, (setter)mobile_set_description},

    # PYUSE_MOBGETSETPROP(sex),
    # PYUSE_MOBGETSETPROP(position),
    # PYUSE_MOBGETPROP(playerflags),
    # PYUSE_MOBGETPROP(npcflags),

    # // XXX Join-these:
    # PYUSE_MOBGETPROP(preferences),
    # PYUSE_MOBGETPROP(preferences2),

    # {"affectflags", (getter)mobile_get_affectvector},
    # PYUSE_MOBGETPROP(affectvector),
    # PYUSE_MOBGETPROP(affections),

    # // What about display-flags?  Maybe it should use mobile_display_flags defined in this file..

    # PYUSE_MOBGETPROP(equipment),
    # PYUSE_MOBGETPROP(inventory),

    # {"fighting", (getter)mobile_get_fighting, (setter)mobile_set_fighting},
    # {"opponent", (getter)mobile_get_fighting, (setter)mobile_set_fighting},

    # PYUSE_MOBGETSETPROP(master),
    # PYUSE_MOBGETPROP(holding),
    # PYUSE_MOBGETPROP(heldby),
    # PYUSE_MOBGETPROP(mount),
    # PYUSE_MOBGETPROP(mountedby),

    # PYUSE_MOBGETPROP(followers),
    # PYUSE_MOBGETPROP(colorset),

    # // {"gender", (getter)mobile_get_gender},
    # // {"sex",    (getter)mobile_get_gender},

    # // {"position", (getter)mobile_get_position},

    # // NPC Mobiles
    # {"__special__", (getter)mobile_get_specproc, (setter)mobile_set_specproc},
    # {"special",     (getter)mobile_get_specproc, (setter)mobile_set_specproc},
    # {"prototype",   (getter)mobile_get_prototype /* Settable! */},

    # {"specialName", (getter)mobile_get_specproc_name},

    # // Player
    # {"mortal",       (getter)mobile_get_ismortal},
    # {"immortal",     (getter)mobile_get_isimmortal},
    # {"god",          (getter)mobile_get_isgod},
    # {"supreme",      (getter)mobile_get_isimpl},
    # {"implementor",  (getter)mobile_get_isimpl},
    # {"isPlayer",     (getter)mobile_isPlayer},

    # // Or Non-player
    # {"npc",          (getter)mobile_get_isnpc},

    # {"alias",         (getter)mobile_get_allaliases,  (setter)mobile_set_allaliases},
    # // {"complex_alias", (getter)mobile_get_cmplxalias,  (setter)mobile_set_cmplxalias},
    # // {"simple_alias",  (getter)mobile_get_smplalias,   (setter)mobile_set_smplalias},

    # // {"check_mail",   (getter)mobile_get_mail},
    # // {"mail",         (getter)mobile_get_mail},
    # {"hasMail",      (getter)mobile_has_mail},

    # {"middleName",   (getter)mobile_get_middlename},

    # {"valid",        (getter)mobile_isvalid},
    # {"destructor",   (getter)mobile_get_destructor, (setter)mobile_set_destructor},

    # // Let's not define this right off: just set it on the dictionary straight.
    # // {"destroy",      (getter)mobile_get_destructor, (setter)mobile_set_destructor},

    # #ifdef EXPOSE_DICT
    #     {"__dict__",           (getter)mobile_get_dict},
    # #elif defined(EXPOSE_DICT_RENAMED)
    #     {EXPOSE_DICT_RENAMED,  (getter)mobile_get_dict},
    # #endif

    # {"power_rating", (getter)mobile_power_rating},
    # {"power",        (getter)mobile_power_rating},

    # {"programming",  (getter)mobile_get_programming, (setter)mobile_set_programming},
    # {"commands",     (getter)mobile_get_trusted_commands},
    # {"trusted",      (getter)mobile_get_trusted_commands},

    # {"armorclass",   (getter)mobile_get_armorclass},
    # {"armor",        (getter)mobile_get_armorclass},

    # {"wizinvis_level", (getter)mobile_get_wizinvis_level},

    # {"store_value",  (getter)mobile_get_playerstore},
    # {"playerstore",  (getter)mobile_get_playerstore},
    # {"store",        (getter)mobile_get_playerstore},

    # {"equipment",    (getter)mobile_get_equipment},

    # {"syslogLevel",  (getter)mobileGetSyslogLevel},

    # {"py_handle",    (getter)NULL, (setter)mobileSetHandle},
    # {"handle",       (getter)NULL, (setter)mobileSetHandle,

    # {"cmdlock",      (getter)mobileGetCmdlock, (setter)mobileSetCmdlock},

    # MINT(pfilepos   ), // int
    # MINT(nr         ), // mob_rnum  (unsigned int)
    # MINT(in_room    ), // room_rnum (unsigned int)
    # MINT(was_in_room), // room_rnum (unsigned int)

    # // Fraun Dec 3rd 2005 - Renamed from 'wait'
    # M(nr, T_INT, "waitState"),

    # { "passwd", T_STRING_INPLACE, offsetof(struct char_data, player.passwd), READONLY },

    # // Getset Descriptor
    # // MNSTR(player.name, "name"),

    # // MNSTR(player.short_descr, "short_descr"),
    # // MNSTR(player.long_descr, "long_descr"),
    # // MNSTR(player.description, "description"),

    # MNSTR(player.title, "title"),
    # MNSTR(player.nickname, "nickname"),
    # MNSTR(player.prename, "prename"),
    # MNSTR(player.wizname, "wizname"),
    # MNSTR(player.plan, "plan"),
    # MNSTR(player.email, "email"),

    # MNINT(player.remort, "remort"), // int -- descriptor?
    # MNINT(player.race, "race"),     // int -- descriptor?
    # MNINT(player.clan, "clan"),     // int -- descriptor?
    # MNINT(player.clanrank, "clanrank"),   // int
    # MNINT(player.save_room, "save_room"), // int
    # MNINT(player.page_length, "page_length"),  // int
    # MNINT(player.breath, "breath"), // int

    # // sex implemented as a descriptor
    # // chclass implemented as a descriptor
    # M(player.level, T_BYTE, "level"), // byte

    # MNINT(player.hometown, "hometown"), // int

    # // struct time_data time;

    # M(player.weight, T_UBYTE, "weight"), // ubyte
    # M(player.height, T_UBYTE, "height"), // ubyte

    # MNINT(player.login_time, "login_time"), // time_t

    # // Reimplement these as descriptors?
    # M(real_abils.str,     T_BYTE, "strength"),           // sbyte
    # M(real_abils.str_add, T_BYTE, "strength_addition"),  // sbyte
    # M(real_abils.intel,   T_BYTE, "intelligence"),       // sbyte
    # M(real_abils.wis,     T_BYTE, "wisdom"),             // sbyte
    # M(real_abils.dex,     T_BYTE, "dexterity"),          // sbyte
    # M(real_abils.con,     T_BYTE, "constitution"),       // sbyte
    # M(real_abils.cha,     T_BYTE, "charisma"),           // sbyte

    # M(aff_abils.str,      T_BYTE, "aff_strength"),           // sbyte
    # M(aff_abils.str_add,  T_BYTE, "aff_strength_addition"),  // sbyte
    # M(aff_abils.intel,    T_BYTE, "aff_intelligence"),       // sbyte
    # M(aff_abils.wis,      T_BYTE, "aff_wisdom"),             // sbyte
    # M(aff_abils.dex,      T_BYTE, "aff_dexterity"),          // sbyte
    # M(aff_abils.con,      T_BYTE, "aff_constitution"),       // sbyte
    # M(aff_abils.cha,      T_BYTE, "aff_charisma"),           // sbyte

    # M(points.mana, T_SHORT, "mana"),
    # M(points.max_mana, T_SHORT, "max_mana"),

    # M(points.hit, T_SHORT, "hit"),
    # M(points.max_hit, T_SHORT, "max_hit"),

    # // I'm dead serious.  See moveMobile, mobile_move, and NotifyMovement.  How about 'stamina?'
    # M(points.move, T_SHORT, "fatigue"),
    # M(points.max_move, T_SHORT, "max_fatigue"),

    # M(points.deaths, T_SHORT, "deaths"),
    # M(points.mkills, T_SHORT, "npckills"),
    # M(points.pkills, T_SHORT, "plrkills"), // inconsistancy with 'playerflags'?
    # M(points.dts, T_SHORT, "dts"),
    # M(points.qpoints, T_SHORT, "qpoints"),

    # // armorclass is computed.  See getset
    # M(points.armor, T_SHORT, "ac"),

    # MNINT(points.gold, "gold_on_hand"),
    # // MNINT(points.bank_gold, "gold_in_bank"),
    # MNINT(points.exp, "experience"),

    # M(points.hitroll, T_BYTE, "hitroll"),
    # M(points.damroll, T_BYTE, "damroll"),

    # MNSTR(char_specials.afk_message, "afk_message"),

    # // XXX Implement wielded_by -- or is this obselete? (temporary magic-casting mobiles as special weapons)

    # // position is implemented as a descriptor

    # MNINT(char_specials.carry_weight, "carry_weight"),
    # M(char_specials.carry_items, T_BYTE, "carry_items"), // byte

    # MNINT(char_specials.timer, "timer"),
    # MNINT(char_specials.arena, "arena"),
    # MNINT(char_specials.tracking, "tracking"),
    # MNINT(char_specials.track_timer, "track_timer"),

    # MNINT(char_specials.saved.alignment, "alignment"),
    # MNINT(char_specials.saved.idnum, "idnum"),

    # // Fraun Sep 30th 2005 - Access these two things through the descriptors
    # // MNINT(char_specials.saved.act, "flags"), // XXX obselete this
    # // MNINT(char_specials.saved.affected_by, "affected_bits"), // XXX obselete this

    # // XXX Implement player-specials separately:
    # //   - act and affected_by covered by npcflags and playerflags
    # //   - sh_int apply_saving_throw[5] getset descriptor

    # M(mob_specials.last_direction, T_BYTE, "last_dir"),

    # MNINT(mob_specials.attack_type, "attack_type"),
    # MNINT(mob_specials.walk_type, "walk_type"),

    # M(mob_specials.default_pos, T_BYTE, "default_pos"),
    # M(mob_specials.damnodice,   T_BYTE, "damnodice"),   // These could change to ints!
    # M(mob_specials.damsizedice, T_BYTE, "damsizedice"), // These could change to ints!

    # MNINT(mob_specials.timer, "timer"),

    # {"perform", (PyCFunction)mobile_perform, METH_VARARGS,
    #  mobile_perform_doc},

    # {"findplayer", (PyCFunction)mobile_findplayer, METH_VARARGS,
    #  mobile_findplayer_doc},
    # {"findchar",   (PyCFunction)mobile_findchar,   METH_VARARGS,
    #  mobile_findchar_doc},
    # {"finditem",   (PyCFunction)mobile_finditem,   METH_VARARGS,
    #  mobile_finditem_doc},

    # {"find",       (PyCFunction)mobile_generic_find, METH_VARARGS|METH_KEYWORDS,
    #  mobileGenericFindDoc},

    # // {"getalias",   (PyCFunction)mobile_getalias,   METH_VARARGS,
    # // mobile_getalias_doc},
    # // {"setalias",   (PyCFunction)mobile_setalias,   METH_VARARGS,
    # // mobile_setalias_doc},

    # {"members", (PyCFunction)mobile_members, METH_NOARGS, ""},

    # // ToDo: implement __contains__ to look in inventory and equipment list, recursing through containers.

    # {"wearing", (PyCFunction)mobileWearing, METH_VARARGS,
    #  "Lookup mobile equipment by position.  Do some other things too."},

    # {"instantiate", (PyCFunction)mobile_instantiate, METH_VARARGS|METH_KEYWORDS,
    #  mobile_instantiate_doc},
    # {"load",        (PyCFunction)mobile_instantiate, METH_VARARGS|METH_KEYWORDS,
    #  mobile_instantiate_doc},
    # {"new",         (PyCFunction)mobile_instantiate, METH_VARARGS|METH_KEYWORDS,
    #  mobile_instantiate_doc},
    # {"read_mobile", (PyCFunction)mobile_instantiate, METH_VARARGS|METH_KEYWORDS,
    #  mobile_instantiate_doc},

    # {"save",        (PyCFunction)mobile_save,        METH_NOARGS,
    #  "Calls save_player on PC/<write_mobproto_to_db> on NPC."},
    # {"unrent",      (PyCFunction)mobile_unrent,       METH_NOARGS,
    #  "Calls StuphAPI_Call(Crash_load) on PC."},
    # {"rent",        (PyCFunction)mobile_rent,         METH_VARARGS,
    #  "Calls Crash_rentsave."},

    # {"save_player_file", (PyCFunction)mobileSavePlayerFile, METH_VARARGS,
    #  ""},

    # {"move",        (PyCFunction)mobile_move,        METH_VARARGS,
    #  "Move a mobile from one room to another.  Same as setting 'room' or 'location'."},

    # {"update_position", (PyCFunction)mobile_update_position, METH_NOARGS, ""},
    # {"sever_limb", (PyCFunction)mobile_sever_limb, METH_VARARGS, ""},

    # {"make_corpse", (PyCFunction)mobile_make_corpse, METH_NOARGS, ""},
    # {"killAlignmentChange", (PyCFunction)mobile_kill_alignment_change, METH_VARARGS, ""},
    # {"deathCry", (PyCFunction)mobile_death_cry, METH_NOARGS, ""},
    # {"rawKill", (PyCFunction)mobile_raw_kill, METH_NOARGS, ""},
    # {"die", (PyCFunction)mobile_die, METH_NOARGS, ""},
    # {"stop_hunting", (PyCFunction)mobile_stop_hunting, METH_VARARGS, ""},
    # {"check_subdue", (PyCFunction)mobile_check_subdue, METH_VARARGS, ""},
    # {"incur_damage", (PyCFunction)mobile_incur_damage, METH_VARARGS, ""},
    # {"get_thac0", (PyCFunction)mobileGetTHAC0, METH_VARARGS,
    #  "Calculates the hit base for this mobile attacking given mobile parameter."},
    # {"attack", (PyCFunction)mobileAttack, METH_VARARGS, ""},
    # {"hit",    (PyCFunction)mobileAttack, METH_VARARGS, ""},
    # {"perform_attack", (PyCFunction)mobilePerformViolence, METH_VARARGS, ""},
    # {"attackModeOrder", (PyCFunction)mobileGetAttackModeOrder, METH_NOARGS, ""},

    # {"checkAutoassist", (PyCFunction)mobileCheckAutoAssist, METH_NOARGS, ""},
    # {"sameAs", (PyCFunction)mobileSameAs, METH_VARARGS, ""},
    # {"eq_apply_ac", (PyCFunction)mobile_eq_apply_ac, METH_VARARGS, ""},
    # {"invalid_item_align", (PyCFunction)mobile_invalid_item_align, METH_VARARGS, ""},

    # {"equip", (PyCFunction)mobileEquip, METH_VARARGS, ""},
    # {"wearing", (PyCFunction)mobileWearing, METH_NOARGS, ""},
    # {"unequip", (PyCFunction)mobileUnequip, METH_VARARGS, ""},

    # {"visibleToLevel", (PyCFunction)mobileVisibleToLevel, METH_VARARGS,
    #  mobileVisibleToLevelDoc},

    # {"visibleBy", (PyCFunction)mobileVisibleBy, METH_VARARGS,
    #  "Can the given mobile see this mobile?\n"},
    # {"canSee",    (PyCFunction)mobileCanSee,    METH_VARARGS,
    #  mobileCanSeeDoc},

    # {"do_auto_exits",  (PyCFunction)mobileDoAutoExits, METH_NOARGS,
    #  "Invokes do_auto_exits."},

    # {"changeHandle",   (PyCFunction)mobileChangeHandle, METH_VARARGS,
    #  "Returns the old reference to the old handle."},

    # {"act", (PyCFunction)mobileAct, METH_VARARGS | METH_KEYWORDS,
    #  mobileActDoc},

    # {"extract", (PyCFunction)mobileExtract, METH_NOARGS},

    # {"tell", (PyCFunction)mobilePerformTell, METH_VARARGS,
    #  "Perform a tell communication directly to target person."},
    # {"reply", (PyCFunction)mobilePerformReply, METH_VARARGS,
    #  "Reply to last target person."},

    # {"sayTo", (PyCFunction)mobilePerformSayTo, METH_VARARGS,
    #  "Perform a room-say directly to target (optional verb parameter at end)."},

    # {"consider", (PyCFunction)mobileConsider, METH_VARARGS,
    #  "Return consideration text between combatants.\n"},

    pass

MobileAdapter = MobileExtensionPoint
